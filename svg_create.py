from svgelements import SVG, Path, Point, Group
import math
import pandas as pd

from svgpathtools import svg2paths2, wsvg
from svgpathtools import Path
from shapely.geometry import Point

from xml.etree import ElementTree as ET
from sqlalchemy import create_engine, insert, Table, MetaData, select, and_
import os

#n_bike_class = "motogp"
#n_year = 2025
#n_race = "ItalianGP"
#n_session = "SPRINT"
#n_session_short = "rac"
def create_svg(n_bike_class, n_year, n_race, n_session, n_session_short, race_id, race):

    
    engine = create_engine("mariadb+mariadbconnector://root:boris123@localhost:3306/motogp")
    metadata = MetaData()

    fastest_laps = Table(
        'fastest_laps',
        metadata,
        autoload_with=engine,
        autoload_replace=True
    )

    entries_all = Table(
        'entries',
        metadata,
        autoload_with=engine,
        autoload_replace=True
    )

    bikes = Table(
        'bikes',
        metadata,
        autoload_replace=True,
        autoload_with=engine
    )

    def find_manual_offset(path, target_point):
        best_offset, min_dist = 0, float('inf')
        # Skeniramo cijelu putanju
        steps = 2000 
        for i in range(steps + 1):
            offset_pct = i / steps
            p = path.point(offset_pct)
            dist = math.sqrt((p.x - target_point.x)**2 + (p.y - target_point.y)**2)
            if dist < min_dist:
                min_dist, best_offset = dist, offset_pct
        return best_offset


    def create_motoslicks_svg_0(INPUT_FILE, OUTPUT_FILE, marker_points, sector_data):
        try:
            full_svg = SVG.parse(INPUT_FILE)
        except Exception as e:
            print(f"Greška pri otvaranju {INPUT_FILE}: {e}")
            return

        main_path_obj = None
        static_elements_xml = []

        for e in full_svg.elements():
            if isinstance(e, Path):
                cls = str(e.values.get('class', ''))
                
                if 'st0' in cls:
                    main_path_obj = e
                else:
                    d_val = e.d()
                    if not d_val or d_val == "None": continue
                    fill = e.values.get('fill', '#444444')
                    static_elements_xml.append(
                        f'  <path d="{d_val}" fill="{fill}" />'
                    )
                    # POPRAVKA: Na bijeloj pozadini koristimo tamno sivu (#444) za brojeve i markere
                    #static_elements_xml.append(
                    #    f'  <path d="{d_val}" fill="#444444" stroke="#444444" opacity="0.8" />'
                    #)
        
        if not main_path_obj:
            print("Greška: Nije pronađena staza sa klasom .st0")
            return

        # 2. EKSTRAKCIJA PRAVE LINIJE STAZA
        # Mnogi Illustrator fajlovi imaju duple linije. Uzimamo onu koja najbolje odgovara markerima.
        all_subpaths = [Path(p) for p in main_path_obj.as_subpaths()]
        
        # Ako je lista prazna nakon filtriranja dužine, sklonite filter ili smanjite prag
        subpaths = [p for p in all_subpaths if p.length() > 10] # Smanjen prag sa 100 na 10

        if not subpaths:
            # Ako i dalje nema ništa, uzmi ceo objekt kao jednu putanju
            track_line = main_path_obj
        else:
            # Biramo subpath koji je najbliži 'start' markeru
            track_line = min(subpaths, key=lambda p: math.dist(p.point(0), marker_points['start']))

        # 3. Mapiranje markera
        offsets = {k: find_manual_offset(track_line, v) for k, v in marker_points.items()}
        
        bounds = [
            (offsets["start"], offsets["s1_end"]),
            (offsets["s1_end"], offsets["s2_end"]),
            (offsets["s2_end"], offsets["s3_end"]),
            (offsets["s3_end"], offsets["start"])
        ]

        sector_paths = []
        text_labels = []
        all_points_for_viewbox = []

        # 4. Generisanje sektora
        for i, (start_pct, end_pct) in enumerate(bounds):
            points = []
            res = 500 
            
            if start_pct > end_pct:
                # Sektor koji siječe kraj/početak (npr. 0.95 -> 0.05)
                steps_to_end = int(res * (1.0 - start_pct))
                for j in range(steps_to_end + 1):
                    t = start_pct + (j/steps_to_end) * (1.0 - start_pct) if steps_to_end > 0 else start_pct
                    points.append(track_line.point(t))
                
                steps_from_start = int(res * end_pct)
                for j in range(1, steps_from_start + 1):
                    t = (j/steps_from_start) * end_pct
                    points.append(track_line.point(t))
            else:
                for j in range(res + 1):
                    t = start_pct + (j/res) * (end_pct - start_pct)
                    points.append(track_line.point(t))
            
            all_points_for_viewbox.extend(points)
            d_str = f"M {points[0].x},{points[0].y} " + " ".join([f"L {p.x},{p.y}" for p in points[1:]])
            
            data = sector_data[i]
            sector_paths.append(
                f'  <path d="{d_str}" fill="none" stroke="{data["color"]}" stroke-width="4.5" stroke-linecap="round" />'
            )

            # Labela na sredini sektora
            mid_idx = len(points) // 2
            mid_p = points[mid_idx]
            text_labels.append(
                f'  <text x="{mid_p.x}" y="{mid_p.y}" font-family="sans-serif" font-size="4.5" font-weight="900" text-anchor="middle" style="paint-order: stroke; stroke: #f0f0f0; stroke-width: 3px;">'
                f'<tspan x="{mid_p.x}" dy="-1.2">{data["rider"]}</tspan>'
                f'<tspan x="{mid_p.x}" dy="5.5" font-size="3.5" font-weight="normal">({data["time"]})</tspan></text>'
            )

        # 5. UNIVERZALNI VIEWBOX (Padding od 15%)
        all_x = [p.x for p in all_points_for_viewbox]
        all_y = [p.y for p in all_points_for_viewbox]
        
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        width = max_x - min_x
        height = max_y - min_y
        
        padding = max(width, height) * 0.15  # 15% paddinga
        
        v_x, v_y = min_x - padding, min_y - padding
        v_w, v_h = width + (padding * 2), height + (padding * 2)
        font_size = "4.5"
        line_height = 5.5
        margin_left = 0
        margin_top = 0
        x_pos = margin_left
        text_xml = f"""
                <text x="{x_pos}" y="{margin_top}" font-family="sans-serif" font-size="{font_size}" font-weight="bold" fill="white" text-anchor="start">
                    <tspan x="{x_pos}" dy="0" fill="#9c9c9d">motoslicks.com</tspan>
                    <tspan x="{x_pos}" dy="{line_height}">{n_bike_class.upper()}</tspan>
                    <tspan x="{x_pos}" dy="{line_height}">{n_session}</tspan>
                    <tspan x="{x_pos}" dy="{line_height}">{n_race} - {n_year}</tspan>
                </text>
                """
        

        # 6. Pisanje fajla
        with open(OUTPUT_FILE, "w") as f:
            f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(f'<svg viewBox="{v_x} {v_y} {v_w} {v_h}" xmlns="http://www.w3.org/2000/svg" style="background:#121212;">\n')
            f.write(f'  <path d="{track_line.d()}" fill="121212" stroke="#ccc" stroke-width="1" opacity="0.5" />\n')
            f.write("\n".join(sector_paths) + "\n")
            f.write("\n".join(text_labels) + "\n")
            f.write("\n".join(static_elements_xml))
            f.write(text_xml)
            f.write("</svg>")
        
        print(f"Uspješno generisano: {OUTPUT_FILE}")

    def create_motoslicks_svg(INPUT_FILE, OUTPUT_FILE, marker_points, sector_data):
        full_svg = SVG.parse(INPUT_FILE)
        main_path_obj = None

        static_elements_xml = []

        for e in full_svg.elements():
            if isinstance(e, Path):
                cls = str(e.values.get('class', ''))
                
                if 'st0' in cls:
                    main_path_obj = e
                else:
                    d_val = e.d()
                    if not d_val or d_val == "None": continue
                    fill = e.values.get('fill', '#444444')
                    # POPRAVKA: Na bijeloj pozadini koristimo tamno sivu (#444) za brojeve i markere
                    static_elements_xml.append(
                        f'  <path d="{d_val}" fill="{fill}" />'
                    )
        
        # Pronalazimo glavni objekt staze
        for e in full_svg.elements():
            if isinstance(e, Path):
                cls = str(e.values.get('class', ''))
                if 'st0' in cls:
                    main_path_obj = e
                    break

        if not main_path_obj:
            print("Greška: Nije pronađena klasa .st0!")
            return

        # KLJUČNO: Uzimamo samo JEDAN krug (vanjsku ivicu) iz compound patha
        subpaths = list(main_path_obj.as_subpaths())
        if not subpaths:
            print("Greška: Putanje su prazne!")
            return
            
        # Uzimamo najduži krug (to je obično vanjska ivica asfalta)
        track_line = Path(max(subpaths, key=lambda p: Path(p).length()))

        # Mapiranje tačaka na tu liniju
        offsets = {k: find_manual_offset(track_line, v) for k, v in marker_points.items()}
        
        # Redoslijed sektora
        bounds = [
            (offsets["start"], offsets["s1_end"]),
            (offsets["s1_end"], offsets["s2_end"]),
            (offsets["s2_end"], offsets["s3_end"]),
            (offsets["s3_end"], offsets["start"])
        ]

        sector_paths = []
        text_labels = []
        all_points_for_viewbox = []

        for i, (start_pct, end_pct) in enumerate(bounds):
            points = []
            res = 300 # Veća rezolucija za glatke krivine
            
            # Logika za "krug oko staze"
            if start_pct > end_pct:
                # Sektor koji prelazi preko 1.0 (kraj putanje)
                for j in range(res + 1):
                    t = start_pct + (j/res) * (1.0 - start_pct)
                    points.append(track_line.point(t))
                for j in range(res + 1):
                    t = (j/res) * end_pct
                    points.append(track_line.point(t))
            else:
                for j in range(res + 1):
                    t = start_pct + (j/res) * (end_pct - start_pct)
                    points.append(track_line.point(t))
            
            all_points_for_viewbox.extend(points)
            d_str = f"M {points[0].x},{points[0].y} " + " ".join([f"L {p.x},{p.y}" for p in points[1:]])
            
            data = sector_data[i]
            # Deblja linija za bolju vidljivost
            sector_paths.append(f'  <path d="{d_str}" fill="none" stroke="{data["color"]}" stroke-width="4" stroke-linecap="round" />')

            # Centriranje teksta na sredinu sektora
            mid_p = points[len(points)//2]
            text_labels.append(
                f'  <text x="{mid_p.x}" y="{mid_p.y}" font-family="Arial, sans-serif" font-size="5" font-weight="bold" text-anchor="middle" style="paint-order: stroke; stroke: white; stroke-width: 2px;">'
                f'<tspan x="{mid_p.x}" dy="-3">{data["rider"]}</tspan>'
                f'<tspan x="{mid_p.x}" dy="6">({data["time"]})</tspan></text>'
            )
            

        # Izračunavanje okvira slike (ViewBox)
        all_x = [p.x for p in all_points_for_viewbox]
        all_y = [p.y for p in all_points_for_viewbox]
        
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        width = max_x - min_x
        height = max_y - min_y
        
        padding = max(width, height) * 0.15  # 15% paddinga
        
        v_x, v_y = min_x - padding, min_y - padding
        v_w, v_h = width + (padding * 2), height + (padding * 2)
        font_size = "4.5"
        line_height = 5.5
        margin_left = 0
        margin_top = 0
        x_pos = margin_left
        text_xml = f"""
                <text x="{x_pos}" y="{margin_top}" font-family="sans-serif" font-size="{font_size}" font-weight="bold" fill="white" text-anchor="start">
                    <tspan x="{x_pos}" dy="0" fill="#9c9c9d">motoslicks.com</tspan>
                    <tspan x="{x_pos}" dy="{line_height}">{n_bike_class.upper()}</tspan>
                    <tspan x="{x_pos}" dy="{line_height}">{n_session}</tspan>
                    <tspan x="{x_pos}" dy="{line_height}">{n_race} - {n_year}</tspan>
                </text>
                """

        with open(OUTPUT_FILE, "w") as f:
            f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(f'<svg viewBox="{v_x} {v_y} {v_w} {v_h}" xmlns="http://www.w3.org/2000/svg" style="background:#121212;">\n')
            f.write(f'  <rect x="{v_x}" y="{v_y}" width="{v_w}" height="{v_h}" fill="#121212" />\n')
            # Prvo iscrtavamo originalnu stazu kao tanku sivu liniju u pozadini
            f.write(f'  <path d="{main_path_obj.d()}" fill="none" stroke="#ddd" stroke-width="0.5" />\n')
            f.write("\n".join(sector_paths) + "\n")
            f.write("\n".join(text_labels) + "\n")
            f.write("\n\n\n")
            f.write("\n".join(static_elements_xml))
            f.write(text_xml)
            f.write("</svg>")
        
        print(f"Uspješno! Fajl sačuvan kao {OUTPUT_FILE}")



    def find_manual_offset(path, target_point):
        best_offset, min_dist = 0, float('inf')
        steps = 2000 
        for i in range(steps + 1):
            offset_pct = i / steps
            p = path.point(offset_pct)
            dist = math.sqrt((p.x - target_point.x)**2 + (p.y - target_point.y)**2)
            if dist < min_dist:
                min_dist, best_offset = dist, offset_pct
        return best_offset

    def create_motoslicks_svg_2(INPUT_FILE, OUTPUT_FILE, marker_points, sector_data):
        full_svg = SVG.parse(INPUT_FILE)
        main_path_obj = None
        
        # Kolekcija za sve originalne putanje (brojevi, strelice, sjenke)
        static_elements_xml = []
        
        # 1. Prvo prolazimo kroz sve elemente da razdvojimo stazu od ukrasa
        all_elements = list(full_svg.elements())
        
        # Pronalazimo stazu (st0) - ona je obično najduža ili ima klasu st0
        for e in all_elements:
            if isinstance(e, Path):
                cls = str(e.values.get('class', ''))
                if 'st0' in cls:
                    main_path_obj = e
                    break
        
        # Fallback ako nema st0 (uzmi najdužu putanju)
        if not main_path_obj:
            paths_only = [e for e in all_elements if isinstance(e, Path) and e.length() > 50]
            if paths_only:
                main_path_obj = max(paths_only, key=lambda p: p.length())

        if not main_path_obj:
            print("Greška: Staza nije pronađena!")
            return

        # 2. Skupljamo SVE OSTALE elemente (st1, st2, st3...)
        for e in all_elements:
            if isinstance(e, Path):
                # Preskačemo glavnu stazu jer ćemo nju iscrtati posebno kao podlogu
                if e == main_path_obj:
                    continue
                
                d_val = e.d()
                if not d_val or d_val == "None": continue
                
                # Izvlačimo boju/stil originalnog elementa
                fill = e.values.get('fill', '#999999') # default siva
                cls = e.values.get('class', '')
                
                # Mapiranje boja na osnovu tvojih klasa iz Illustratora
                # (Ovo omogućava da strelice ostanu crvene, a brojevi bijeli/sivi)
                color_map = {
                    'st1': '#C80502', # Crvena (strelice)
                    'st2': '#FFFFFF', # Bijela (brojevi unutar krugova)
                    'st3': '#171C21', # Tamna
                    'st4': '#00B753', # Zelena
                    'st6': '#1D1D1B', # Crna
                }
                final_fill = color_map.get(cls, fill)
                
                static_elements_xml.append(
                    f'  <path d="{d_val}" fill="{final_fill}" stroke="none" />'
                )

        # 3. Obrada linije za sektore (isto kao prije)
        subpaths = list(main_path_obj.as_subpaths())
        track_line = Path(max(subpaths, key=lambda p: Path(p).length()))
        offsets = {k: find_manual_offset(track_line, v) for k, v in marker_points.items()}
        
        bounds = [
            (offsets["start"], offsets["s1_end"]),
            (offsets["s1_end"], offsets["s2_end"]),
            (offsets["s2_end"], offsets["s3_end"]),
            (offsets["s3_end"], offsets["start"])
        ]

        sector_paths = []
        text_labels = []
        all_points_for_viewbox = []

        for i, (start_pct, end_pct) in enumerate(bounds):
            points = []
            res = 400
            if start_pct > end_pct:
                for j in range(res + 1):
                    t = start_pct + (j/res) * (1.0 - start_pct)
                    points.append(track_line.point(t))
                for j in range(res + 1):
                    t = (j/res) * end_pct
                    points.append(track_line.point(t))
            else:
                for j in range(res + 1):
                    t = start_pct + (j/res) * (end_pct - start_pct)
                    points.append(track_line.point(t))
            
            all_points_for_viewbox.extend(points)
            d_str = f"M {points[0].x},{points[0].y} " + " ".join([f"L {p.x},{p.y}" for p in points[1:]])
            
            data = sector_data[i]
            sector_paths.append(f'  <path d="{d_str}" fill="none" stroke="{data["color"]}" stroke-width="3.5" stroke-linecap="round" />')

            mid_p = points[len(points)//2]
            text_labels.append(
                f'  <text x="{mid_p.x}" y="{mid_p.y}" font-family="Arial, sans-serif" font-size="4.5" font-weight="bold" text-anchor="middle" style="paint-order: stroke; stroke: #f0f0f0; stroke-width: 2.5px;">'
                f'<tspan x="{mid_p.x}" dy="-2.5">{data["rider"]}</tspan>'
                f'<tspan x="{mid_p.x}" dy="5.5">({data["time"]})</tspan></text>'
            )

        # 4. Finalni upis (ViewBox uzimamo iz originalnog SVG-a da razmjer ostane isti)
        all_x = [p.x for p in all_points_for_viewbox]
        all_y = [p.y for p in all_points_for_viewbox]
        
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        width = max_x - min_x
        height = max_y - min_y
        
        padding = max(width, height) * 0.15  # 15% paddinga
        
        v_x, v_y = min_x - padding, min_y - padding
        v_w, v_h = width + (padding * 2), height + (padding * 2)
        viewbox = f"0 0 170.6 210.3"
        font_size = "4.5"
        line_height = 5.5
        margin_left = 0
        margin_top = 0
        x_pos = margin_left
        text_xml = f"""
                <text x="{x_pos}" y="{margin_top}" font-family="sans-serif" font-size="{font_size}" font-weight="bold" fill="white" text-anchor="start">
                    <tspan x="{x_pos}" dy="0" fill="#9c9c9d">motoslicks.com</tspan>
                    <tspan x="{x_pos}" dy="{line_height}">{n_bike_class.upper()}</tspan>
                    <tspan x="{x_pos}" dy="{line_height}">{n_session}</tspan>
                    <tspan x="{x_pos}" dy="{line_height}">{n_race} - {n_year}</tspan>
                </text>
                """

        with open(OUTPUT_FILE, "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(f'<svg viewBox="{v_x} {v_y} {v_w} {v_h}" xmlns="http://www.w3.org/2000/svg" style="background:#121212;">\n')
            f.write(f'  <rect x="{v_x}" y="{v_y}" width="{v_w}" height="{v_h}" fill="#121212" />\n')
            
            # Redoslijed slojeva:
            # 1. Glavna staza (blijedo siva)
            f.write(f'  \n')
            f.write(f'  <path d="{main_path_obj.d()}" fill="#121212" stroke="none" />\n')
            
            # 2. Svi statični elementi (brojevi, strelice st1, st2...)
            f.write(f'  \n')
            f.write("\n".join(static_elements_xml) + "\n")
            
            # 3. Obojeni sektori (preko svega)
            f.write(f'  \n')
            f.write("\n".join(sector_paths) + "\n")
            
            # 4. Tekstualne oznake
            f.write("\n".join(text_labels) + "\n")
            f.write(text_xml)
            f.write("</svg>")
        print(f"Uspješno generisan SVG sa svim elementima: {OUTPUT_FILE}")

    from svgelements import SVG, Path, Group, Point

    from svgelements import SVG, Path, Group, Point

    def create_motoslicks_svg_3(INPUT_FILE, OUTPUT_FILE, marker_points, sector_data):
        full_svg = SVG.parse(INPUT_FILE)
        all_points_for_viewbox = []
        # 1. Pronalaženje najduže putanje (staze)
        all_paths = [e for e in full_svg.elements() if isinstance(e, Path) and e.d() and e.d() != "None"]
        if not all_paths:
            print("Greška: SVG ne sadrži putanje!")
            return
        main_path_obj = max(all_paths, key=lambda p: p.length())

        static_elements_xml = []
        def process_elements(elements):
            for e in elements:
                if isinstance(e, Group):
                    process_elements(e)
                    continue
                if e == main_path_obj:
                    continue
                if hasattr(e, 'd'):
                    d_val = e.d()
                    if d_val and d_val != "None":
                        fill = e.values.get('fill', '#444444')
                        static_elements_xml.append(
                            f'  <path d="{d_val}" fill="{fill}" opacity="0.6" />'
                        )

        process_elements(full_svg.elements())

        # 2. Ekstrakcija linije za sektore
        subpaths = list(main_path_obj.as_subpaths())
        track_line = Path(max(subpaths, key=lambda p: Path(p).length()))

        # --- ISPRAVLJEN DIO: Zamjena za .project() ---
        def get_pct(pt):
            # Uzorkujemo stazu u 1000 tačaka i tražimo onu koja je najbliža zadatom markeru
            precision = 1000 
            best_t = 0
            min_dist = float('inf')
            
            for i in range(precision + 1):
                t = i / precision
                p = track_line.point(t)
                # Distanca između dvije tačke (Pitagora)
                dist = ((p.x - pt.x)**2 + (p.y - pt.y)**2)**0.5
                if dist < min_dist:
                    min_dist = dist
                    best_t = t
            return best_t
        # ---------------------------------------------

        offsets = {
            "start": get_pct(marker_points['start']),
            "s1_end": get_pct(marker_points['s1_end']),
            "s2_end": get_pct(marker_points['s2_end']),
            "s3_end": get_pct(marker_points['s3_end'])
        }
        
        bounds = [
            (offsets["start"], offsets["s1_end"]),
            (offsets["s1_end"], offsets["s2_end"]),
            (offsets["s2_end"], offsets["s3_end"]),
            (offsets["s3_end"], offsets["start"])
        ]

        sector_paths = []
        text_labels = []

        for i, (end_pct, start_pct) in enumerate(bounds):
            points = []
            res = 400
            if start_pct > end_pct:
                for j in range(res + 1):
                    t = start_pct + (j/res) * (1.0 - start_pct)
                    points.append(track_line.point(t))
                for j in range(res + 1):
                    t = (j/res) * end_pct
                    points.append(track_line.point(t))
            else:
                for j in range(res + 1):
                    t = start_pct + (j/res) * (end_pct - start_pct)
                    points.append(track_line.point(t))
            
            d_str = f"M {points[0].x},{points[0].y} " + " ".join([f"L {p.x},{p.y}" for p in points[1:]])
            data = sector_data[i]
            sector_paths.append(f'  <path d="{d_str}" fill="none" stroke="{data["color"]}" stroke-width="3.5" stroke-linecap="round" />')
            all_points_for_viewbox.extend(points)
            mid_p = points[len(points)//2]
            text_labels.append(
                f'  <text x="{mid_p.x}" y="{mid_p.y}" font-family="Arial, sans-serif" font-size="5" font-weight="bold" text-anchor="middle" style="paint-order: stroke; stroke: white; stroke-width: 2px;">'
                f'<tspan x="{mid_p.x}" dy="-3">{data["rider"]}</tspan>'
                f'<tspan x="{mid_p.x}" dy="6">({data["time"]})</tspan></text>'
            )

        all_x = [p.x for p in all_points_for_viewbox]
        all_y = [p.y for p in all_points_for_viewbox]
        
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        width = max_x - min_x
        height = max_y - min_y
        
        padding = max(width, height) * 0.15  # 15% paddinga
        
        v_x, v_y = min_x - padding, min_y - padding
        v_w, v_h = width + (padding * 2), height + (padding * 2)

        font_size = "4.5"
        line_height = 5.5
        margin_left = 0
        margin_top = 0
        x_pos = margin_left
        text_xml = f"""
                <text x="{x_pos}" y="{margin_top}" font-family="sans-serif" font-size="{font_size}" font-weight="bold" fill="white" text-anchor="start">
                    <tspan x="{x_pos}" dy="0" fill="#9c9c9d">motoslicks.com</tspan>
                    <tspan x="{x_pos}" dy="{line_height}">{n_bike_class.upper()}</tspan>
                    <tspan x="{x_pos}" dy="{line_height}">{n_session}</tspan>
                    <tspan x="{x_pos}" dy="{line_height}">{n_race} - {n_year}</tspan>
                </text>
                """

        with open(OUTPUT_FILE, "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(f'<svg viewBox="{v_x} {v_y} {v_w} {v_h}" xmlns="http://www.w3.org/2000/svg" style="background:#121212;">\n')
            f.write(f'  <path d="{main_path_obj.d()}" fill="#121212" />\n')
            f.write("\n".join(static_elements_xml) + "\n")
            f.write("\n".join(sector_paths) + "\n")
            f.write("\n".join(text_labels) + "\n")
            f.write(text_xml)
            f.write("</svg>")

    svg_df = pd.read_csv('/home/boris/Documents/matplotlib_exercize/svg_circuit.csv')
    svg_df = svg_df[svg_df['race'] == race]
    if svg_df.empty:
        return 0
    print(svg_df)
    for i, row in svg_df.iterrows():
        select_fl = select(fastest_laps).where(
                    and_(fastest_laps.c.race_id == race_id, fastest_laps.c.session == n_session_short, fastest_laps.c.bike_class == n_bike_class))
        with engine.connect() as conn:
            result = conn.execute(select_fl).fetchone()

        svg_path = '/home/boris/Documents/matplotlib_exercize/svg_circuit/' + row['race'] + '.svg'
        marker_points = {
            "start": Point(float(row['start'].split('-')[0]), float(row['start'].split('-')[1])),
            "s1_end": Point(float(row['s1_end'].split('-')[0]), float(row['s1_end'].split('-')[1])),
            "s2_end": Point(float(row['s2_end'].split('-')[0]), float(row['s2_end'].split('-')[1])),
            "s3_end": Point(float(row['s3_end'].split('-')[0]), float(row['s3_end'].split('-')[1]))
        }

        racers = [(result.sector_1_racer, n_bike_class, n_year), (result.sector_2_racer, n_bike_class, n_year), (result.sector_3_racer, n_bike_class, n_year), (result.sector_4_racer, n_bike_class, n_year
                                                                                                                                                                )]
        bike_colors = []
        for r in racers:
            select_bike_id = select(entries_all.c.bike_id).where(
                and_(entries_all.c.rider_name == r[0], entries_all.c.bike_class == r[1], entries_all.c.year == r[2]))
            with engine.connect() as conn:
                bike_id = conn.execute(select_bike_id).fetchone()
                if bike_id:
                    select_bike_name = select(bikes.c.hex_color).where(bikes.c.id == bike_id[0])
                    bike_name = conn.execute(select_bike_name).fetchone()
                    bike_colors.append(bike_name[0])

        sector_data = [
                {"name": "Sector 1", "rider": result.sector_1_racer, "time": result.sector_1, "color": bike_colors[0] if len(bike_colors) > 0 else "#9baee4"},
                {"name": "Sector 2", "rider": result.sector_2_racer, "time": result.sector_2, "color": bike_colors[1] if len(bike_colors) > 1 else "#9baee4"},
                {"name": "Sector 3", "rider": result.sector_3_racer, "time": result.sector_3, "color": bike_colors[2] if len(bike_colors) > 2 else "#262626"},
                {"name": "Sector 4", "rider": result.sector_4_racer, "time": result.sector_4, "color": bike_colors[3] if len(bike_colors) > 3 else "#9baee4"},
            ]
        
        
        if row['dones'] == 1:
            create_motoslicks_svg(svg_path, f'/home/boris/Documents/matplotlib_exercize/svg_circuit/svg_{row["race"]}.svg', marker_points, sector_data)
            
        if row['dones'] == 0:
            create_motoslicks_svg_0(svg_path, f'/home/boris/Documents/matplotlib_exercize/svg_circuit/svg_{row["race"]}.svg', marker_points, sector_data)
        if row['dones'] == 2:
            create_motoslicks_svg_2(svg_path, f'/home/boris/Documents/matplotlib_exercize/svg_circuit/svg_{row["race"]}.svg', marker_points, sector_data)
        if row['dones'] == 3:
            create_motoslicks_svg_3(svg_path, f'/home/boris/Documents/matplotlib_exercize/svg_circuit/svg_{row["race"]}.svg', marker_points, sector_data)