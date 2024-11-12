import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
import mpld3


xrange = range

def countIterationsUntilDivergent(c, threshold):
    z = 0
    for iteration in xrange(threshold):
        z = z * z + c
        if abs(z) > 4:
            break
    return iteration

def mandelbrot(threshold, density, center_real, center_imag, zoom, setcmap="hot"):
    # Calculate the range based on the center coordinates and zoom level
    scale = 1 / zoom
    real_axis = np.linspace(center_real - scale, center_real + scale, density)
    imag_axis = np.linspace(center_imag - scale, center_imag + scale, density)
    real_len = len(real_axis)
    imag_len = len(imag_axis)

    atlas = np.empty((real_len, imag_len))

    for ix in xrange(real_len):
        for iy in xrange(imag_len):
            c = complex(real_axis[ix], imag_axis[iy])
            atlas[ix, iy] = countIterationsUntilDivergent(c, threshold)

    fig, ax = plt.subplots()
    ax.imshow(atlas.T, extent=[real_axis.min(), real_axis.max(), imag_axis.min(), imag_axis.max()], interpolation="nearest", cmap=setcmap, origin="lower", )
    ax.axis("off")
    plt.close(fig)
    components.html(mpld3.fig_to_html(fig), height=600, width=800)

st.title("Mandelbrot Set Explorer")
threshold = st.slider("Threshold", 0, 1000, 100)
density = st.slider("Density", 100, 1000, 500)
center_real = st.number_input("Center Real Coordinate", value=-0.5)
center_imag = st.number_input("Center Imaginary Coordinate", value=0.0)
zoom = st.slider("Zoom Level", 1.0, 500.0, 1.0)
cmapselection = st.selectbox("Select a colormap", ["hot", "viridis", "inferno", "plasma", "magma"])

mandelbrot(threshold, density, center_real, center_imag, zoom, cmapselection)
