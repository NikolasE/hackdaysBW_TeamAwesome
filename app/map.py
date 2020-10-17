def build_map():
    svg_map = """
<svg id="svg-object" width="455" height="1000" xmlns="http://www.w3.org/2000/svg">
<rect width="500" height="1000" style="fill:white;stroke-width:3;stroke:rgb(0,0,0)" />

<!-- Kasse, Eingang -->
<rect x="0" y="900" width="200" height="150" style="fill:black;stroke:black;stroke-width:5;fill-opacity:0.3;stroke-opacity:1" />
<rect x="250" y="800" width="2500" height="100" style="fill:black;stroke:black;stroke-width:5;fill-opacity:0.3;stroke-opacity:1" />
<text x="25" y="960" fill="#003278" font-size="2.5em">Eingang</text>
<text x="280" y="865" fill="#003278" font-size="3em">Kasse</text>

<!-- Ganz Links -->
<rect x="0" y="450" width="25" height="400" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="0" y="75" width="25" height="325" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- ganz Oben -->
<rect x="0" y="0" width="450" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Oben 4 -->
<rect x="425" y="75" width="25" height="325" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Oben 3 -->
<rect x="300" y="75" width="25" height="150" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="325" y="75" width="25" height="150" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="300" y="300" width="25" height="75" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="325" y="300" width="25" height="75" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="300" y="275" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="300" y="375" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Oben  2-->
<rect x="200" y="75" width="50" height="175" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="200" y="300" width="50" height="100" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Oben 1 -->
<rect x="100" y="75" width="25" height="125" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="125" y="75" width="25" height="125" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="100" y="250" width="50" height="125" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="100" y="375" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Unten 4 -->
<rect x="425" y="450" width="25" height="300" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Unten 3 -->
<rect x="300" y="475" width="25" height="250" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="325" y="475" width="25" height="250" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="300" y="450" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="300" y="725" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Unten 2 -->
<rect x="100" y="475" width="25" height="250" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="125" y="475" width="25" height="250" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="100" y="450" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="100" y="725" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Unten 1 -->
<rect x="200" y="475" width="25" height="250" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="225" y="475" width="25" height="250" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="200" y="450" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="200" y="725" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Unten 4 -->
<rect x="100" y="800" width="100" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="100" y="825" width="100" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
    
<!-- Location -->
<polygon points="60,850 20,780 100,780" id="location" style="fill:#ffe300;stroke:#003278;stroke-width:5" />
<circle cx="60" cy="850" r="20" stroke="#003278" stroke-width="5" fill="#ffe300"  />    
"""

    svg_end = """</svg>"""
    svg = svg_map + svg_end
    
    return svg
