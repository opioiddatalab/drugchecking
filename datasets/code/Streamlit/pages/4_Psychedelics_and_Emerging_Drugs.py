from load_css import local_css
local_css("datasets/code/Streamlit/pages/psychedelics.css")
local_css("datasets/code/Streamlit/style.css")
from streamlit_elements import elements, mui, html

with elements("nested_children"):
  with elements("properties"):
    with elements("style_mui_sx"):
      with mui.Paper(elevation=12, variant="outlined", sx={
          "padding": "0 1rem 1rem",
          "background-color": "#e39b33",
          "text-align": "center",
          "margin": "0 auto 50px",
        }):
          html.h5("Sample ID: 123456")
          with mui.Paper(elevation=12, variant="outlined", sx={
                        "padding": ".5rem",
                        "margin-top": "-1.25rem",
                        "text-align": "left",
                        "font-size": ".95rem",
                        "background-color": "white"
                      }):
                  with mui.Grid(container=True):
                    with mui.Grid(item=True, xs=8):
                      html.p("Orange County, NC")
                    with mui.Grid(item=True, xs=4):
                      html.p("Medicaid Region #6")
                  html.hr()
                  html.h5("Expected Substances")
                  with mui.Grid(container=True, spacing=2):
                    with mui.Grid(item=True, xs=12):
                      html.p("methamphetamine")
                    with mui.Grid(item=True, xs=12):
                      html.p("acetylcodeine")
                  html.hr()
                  with mui.Container():
                      with mui.Grid(container=True):
                        with mui.Grid(item=True, xs=3):
                          mui.Typography("Lab Results")
                        with mui.Grid(item=True, xs=9):
                          mui.icon.Science()
                      with mui.Grid(container=True):
                        with mui.Grid(item=True, xs=6):
                          mui.icon.VerticalAlignTopRounded()
                          mui.Typography("Primary")
                          mui.Chip(label="fentanyl", variant="outlined")
                          mui.Chip(label="methamphetamine", variant="outlined")
                        with mui.Grid(item=True, xs=6):
                          mui.icon.VerticalAlignBottomRounded()
                          mui.Typography("Trace")
                          mui.Chip(label="quinine", variant="filled")
                          mui.Chip(label="4-ANPP", variant="outlined")
                          mui.Chip(label="lidocaine", variant="outlined")
                          mui.Chip(label="ethyl-4-ANPP", variant="outlined")
                          mui.Chip(label="phenethyl 4-ANPP", variant="outlined")
                      html.h5("Description")
                      html.p("Click a tagged substance to learn more: ")
                      with mui.Paper(elevation=24, variant="outlined", sx={
                        "padding": ".1rem",
                        "text-align": "left",
                        "font-size": ".95rem",
                        "background-color": "pink"
                      }):
                         html.p("An alkaloid derived from the bark of the cinchona tree. It is used as an antimalarial drug, and is the active ingredient in extracts of the cinchona that have been used for that purpose since before 1633. Quinine is also a mild antipyretic and analgesic and has been used in common cold preparations for that purpose. It was used commonly and as a bitter and flavoring agent, and is still useful for the treatment of babesiosis. Quinine is also useful in some muscular disorders, especially nocturnal leg cramps and myotonia congenita, because of its direct effects on muscle membrane and sodium channels. The mechanisms of its antimalarial effects are not well understood.")
                  html.hr()
                  with mui.Paper(elevation=24, variant="outlined", sx={
                        "padding": ".25rem",
                        "margin": "0 .25rem",
                        "font-size": ".95rem",
                        "background-color": "lightblue"
                      }):
                     html.h5("Physical Descriptions:")
                     html.ul([html.li("White"), html.li("Green"), html.li("Crystals; Powder")])
                  mui.icon.Share()
                  html.h5("Share this sample's result")
                  html.hr()
                  with mui.Grid(container=True, spacing=4):
                    with mui.Grid(item=True, xs=6):
                      mui.Button("Hide Sample", variant="outlined", color="info", size="large", sx={"width": "100%"})
                    with mui.Grid(item=True, xs=6):
                      mui.Button("View More Info", variant="contained", color="info", size="large", sx={"width": "100%"})


                  mui.Collapse(in_=True)

