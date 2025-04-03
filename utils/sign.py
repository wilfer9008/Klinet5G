import streamlit as st
#TODO: Add Janniks Github Acc
def sign():
    
    return st.markdown(
    """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: left;
    padding-left: 340px;
}
</style>
<div class="footer">
<span style="color: black; text-decoration: none;">&copy MotionMiners GmbH</span>
<a href="https://github.com/aetherspritee">Dustin Schauten</a>
<a href="https://github.com/wilfer9008">Fernando Moya</a>
<a href="">Jannik Wolff</a>
<a href="https://github.com/rrajevan">Rajevan Raveendran</a>
</div>
""",
    unsafe_allow_html=True,
)
