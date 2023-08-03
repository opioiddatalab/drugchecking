from load_css import local_css
local_css("datasets/code/Streamlit/style.css")
local_css("datasets/code/Streamlit/pages/psychedelics.css")
from streamlit_elements import elements, mui, html, dashboard
import streamlit as st
from persist import persist, load_widget_state
import webbrowser

def main():
    if "alpha_PERSIST" not in st.session_state:
        # Initialize session state.
        st.session_state.update({
            # Default page.
            "checkbox": False,
        })
    else:
        st.session_state.update({
            # Default page.
            "checkbox": True,
        })

if __name__ == "__main__":
    load_widget_state()
    main()

if 'first_PERSIST' not in st.session_state:
   st.session_state['first_PERSIST'] = False
if 'second_PERSIST' not in st.session_state:
   st.session_state['second_PERSIST'] = False
if 'third_PERSIST' not in st.session_state:
   st.session_state['third_PERSIST'] = False


def form_callback():
    st.session_state.first_PERSIST = not st.session_state.first_PERSIST
def form_callback2():
    st.session_state.second_PERSIST = not st.session_state.second_PERSIST
def form_callback3():
    st.session_state.third_PERSIST = not st.session_state.third_PERSIST
def safeSupplyResults():
  js = 'https://www.streetsafe.supply/results/p/801908'
  webbrowser.open(js)


with elements("dashboard"):
  if st.session_state['first_PERSIST'] == False:
    layout = [
          # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
          dashboard.Item("first_item", 0, 0, 3.5, 2.15),
          dashboard.Item("second_item", 4, 0, 3.5, 2.15),
          dashboard.Item("third_item", 8, 0, 3.5, 2.15),
    ]
  if st.session_state['second_PERSIST'] == False:
    layout = [
          # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
          dashboard.Item("first_item", 0, 0, 3.5, 2.15),
          dashboard.Item("second_item", 4, 0, 3.5, 6.5),
          dashboard.Item("third_item", 8, 0, 3.5, 2.15),
    ]
  if st.session_state['third_PERSIST'] == False:
    layout = [
          # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
          dashboard.Item("first_item", 0, 0, 3.5, 2.15),
          dashboard.Item("second_item", 4, 0, 3.5, 2.15),
          dashboard.Item("third_item", 8, 0, 3.5, 6.5),
    ]
  else:
    layout = [
          # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
          dashboard.Item("first_item", 0, 0, 3.5, 6.5),
          dashboard.Item("second_item", 4, 0, 3.5, 6.5),
          dashboard.Item("third_item", 8, 0, 3.5, 6.5),
    ]

  with dashboard.Grid(layout):
    with mui.Paper(key="first_item"):
      with elements("nested_children3"):
            with elements("properties"):
              with elements("style_mui_sx"):
                with mui.Paper(elevation=12, variant="outlined", sx={
                    "padding": "0 1rem 0",
                    "background-color": "#e39b33",
                    "text-align": "center",
                  }):
                    html.h5("Sample ID: 456789")
                    with mui.Paper(elevation=12, variant="outlined", sx={
                                  "padding": ".1rem .5rem",
                                  "text-align": "left",
                                  "font-size": ".95rem",
                                  "background-color": "white"
                                }):
                        with mui.Grid(container=True):
                              with mui.Grid(item=True, xs=5, sx={"text-align": "left"}):
                                html.p("Durham County, NC")
                                html.p("Medicaid Region #6")
                              with mui.Grid(item=True, xs=7, sx={"text-align": "right"}):
                                html.p("Aug 1, 2023")
                        html.hr()
                        html.h5("Expected Substances")
                        html.p("heroin")
                        html.p("fentanyl")
                        with mui.FormControlLabel(label="Show/Hide Lab Data", control=mui.Checkbox(key=persist('first'), onChange=form_callback)):
                          html.hr()
                        html.hr()
                        if st.session_state['first_PERSIST'] == True:
                            st.container()
                            # with mui.Container():
                              # with mui.Grid(container=True"):
                                # with mui.Grid(item=True, xs=3):
                            mui.Typography("Lab Results")
                                # with mui.Grid(item=True, xs=9):
                                #   mui.icon.Science()
                            with mui.Grid(container=True):
                                with mui.Grid(item=True, xs=6):
                                  # mui.icon.VerticalAlignTopRounded()
                                  html.p("Primary")
                                  mui.Chip(label="fentanyl", variant="filled")
                                with mui.Grid(item=True, xs=6):
                                  # mui.icon.VerticalAlignBottomRounded()
                                  html.p("Trace")
                                  mui.Chip(label="quinine", variant="outlined")
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
                                "background-color": "lightgray",
                                "margin": "0 auto",
                                "width": "100%"
                              }):
                                html.p("Fentanyl common potent opioid")
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
                            # with mui.Grid(container=True, spacing=4):
                              # with mui.Grid(item=True, xs=6):
                            # add space between buttons in the ButtonGroup
                            with mui.ButtonGroup(fullWidth=True, sx={"width": "100%"}):
                                mui.Button("Hide Lab Data", variant="contained", color="info", size="small", sx={"width": "50%", "margin": "10px"}, onClick=form_callback)
                              # with mui.Grid(item=True, xs=6):
                                mui.Button("View More Info", variant="contained", color="info", size="small", sx={"width": "50%",  "margin": "10px", "backgroundColor": "#1E2C4A"}, onClick=safeSupplyResults)
                                mui.Collapse(in_=True)
                        else:
                          st.echo('')
    with mui.Paper(key="second_item"):
      with elements("nested_children3"):
            with elements("properties"):
              with elements("style_mui_sx"):
                with mui.Paper(elevation=12, variant="outlined", sx={
                    "padding": "0 1rem 0",
                    "background-color": "#e39b33",
                    "text-align": "center",
                  }):
                    html.h5("Sample ID: 456789")
                    with mui.Paper(elevation=12, variant="outlined", sx={
                                  "padding": ".1rem .5rem",
                                  "text-align": "left",
                                  "font-size": ".95rem",
                                  "background-color": "white"
                                }):
                        with mui.Grid(container=True):
                              with mui.Grid(item=True, xs=5, sx={"text-align": "left"}):
                                html.p("Durham County, NC")
                                html.p("Medicaid Region #6")
                              with mui.Grid(item=True, xs=7, sx={"text-align": "right"}):
                                html.p("Aug 1, 2023")
                        html.hr()
                        html.h5("Expected Substances")
                        html.p("heroin")
                        html.p("fentanyl")
                        with mui.FormControlLabel(label="Show/Hide Lab Data", control=mui.Checkbox(key=persist('second'), onChange=form_callback2)):
                          html.hr()
                        html.hr()
                        if st.session_state['second_PERSIST'] == True:
                            st.container()
                            # with mui.Container():
                              # with mui.Grid(container=True"):
                                # with mui.Grid(item=True, xs=3):
                            mui.Typography("Lab Results")
                                # with mui.Grid(item=True, xs=9):
                                #   mui.icon.Science()
                            with mui.Grid(container=True):
                                with mui.Grid(item=True, xs=6):
                                  # mui.icon.VerticalAlignTopRounded()
                                  html.p("Primary")
                                  mui.Chip(label="fentanyl", variant="filled")
                                with mui.Grid(item=True, xs=6):
                                  # mui.icon.VerticalAlignBottomRounded()
                                  html.p("Trace")
                                  mui.Chip(label="quinine", variant="outlined")
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
                                "background-color": "lightgray",
                                "margin": "0 auto",
                                "width": "100%"
                              }):
                                html.p("Fentanyl common potent opioid")
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
                            # with mui.Grid(container=True, spacing=4):
                              # with mui.Grid(item=True, xs=6):
                            # add space between buttons in the ButtonGroup
                            with mui.ButtonGroup(fullWidth=True, sx={"width": "100%"}):
                                mui.Button("Hide Lab Data", variant="contained", color="info", size="small", sx={"width": "50%", "margin": "10px"}, onClick=form_callback)
                              # with mui.Grid(item=True, xs=6):
                                mui.Button("View More Info", variant="contained", color="info", size="small", sx={"width": "50%",  "margin": "10px", "backgroundColor": "#1E2C4A"}, onClick=safeSupplyResults)
                                mui.Collapse(in_=True)
                        else:
                          st.echo('')
    with mui.Paper(key="third_item"):
      with elements("nested_children3"):
            with elements("properties"):
              with elements("style_mui_sx"):
                with mui.Paper(elevation=12, variant="outlined", sx={
                    "padding": "0 1rem 0",
                    "background-color": "#e39b33",
                    "text-align": "center",
                  }):
                    html.h5("Sample ID: 456789")
                    with mui.Paper(elevation=12, variant="outlined", sx={
                                  "padding": ".1rem .5rem",
                                  "text-align": "left",
                                  "font-size": ".95rem",
                                  "background-color": "white"
                                }):
                        with mui.Grid(container=True):
                              with mui.Grid(item=True, xs=5, sx={"text-align": "left"}):
                                html.p("Durham County, NC")
                                html.p("Medicaid Region #6")
                              with mui.Grid(item=True, xs=7, sx={"text-align": "right"}):
                                html.p("Aug 1, 2023")
                        html.hr()
                        html.h5("Expected Substances")
                        html.p("heroin")
                        html.p("fentanyl")
                        with mui.FormControlLabel(label="Show/Hide Lab Data", control=mui.Checkbox(key=persist('third'), onChange=form_callback3)):
                          html.hr()
                        html.hr()
                        if st.session_state['third_PERSIST'] == True:
                            st.container()
                            # with mui.Container():
                              # with mui.Grid(container=True"):
                                # with mui.Grid(item=True, xs=3):
                            mui.Typography("Lab Results")
                                # with mui.Grid(item=True, xs=9):
                                #   mui.icon.Science()
                            with mui.Grid(container=True):
                                with mui.Grid(item=True, xs=6):
                                  # mui.icon.VerticalAlignTopRounded()
                                  html.p("Primary")
                                  mui.Chip(label="fentanyl", variant="filled")
                                with mui.Grid(item=True, xs=6):
                                  # mui.icon.VerticalAlignBottomRounded()
                                  html.p("Trace")
                                  mui.Chip(label="quinine", variant="outlined")
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
                                "background-color": "lightgray",
                                "margin": "0 auto",
                                "width": "100%"
                              }):
                                html.p("Fentanyl common potent opioid")
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
                            # with mui.Grid(container=True, spacing=4):
                              # with mui.Grid(item=True, xs=6):
                            # add space between buttons in the ButtonGroup
                            with mui.ButtonGroup(fullWidth=True, sx={"width": "100%"}):
                                mui.Button("Hide Lab Data", variant="contained", color="info", size="small", sx={"width": "50%", "margin": "10px"}, onClick=form_callback)
                              # with mui.Grid(item=True, xs=6):
                                mui.Button("View More Info", variant="contained", color="info", size="small", sx={"width": "50%",  "margin": "10px", "backgroundColor": "#1E2C4A"}, onClick=safeSupplyResults)
                                mui.Collapse(in_=True)
                        else:
                          st.echo('')
