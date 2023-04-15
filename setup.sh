#!/bin/bash

# Get the current version of the Streamlit executable
STREAMLIT_VERSION=$(streamlit --version)

# Add Streamlit to the allow list
echo "web: $STREAMLIT_VERSION" > ~/.streamlit/config.toml

# Create directories required for Streamlit
mkdir -p ~/.streamlit
touch ~/.streamlit/credentials.toml
touch ~/.streamlit/config.toml

# Set up the credentials file
echo "[general]" > ~/.streamlit/credentials.toml
echo "email = \"m.gabr@aucegypt.edu\"" >> ~/.streamlit/credentials.toml

# Set up the config file
echo "[server]" > ~/.streamlit/config.toml
echo "headless = true" >> ~/.streamlit/config.toml
echo "enableCORS=false" >> ~/.streamlit/config.toml
echo "port = $PORT" >> ~/.streamlit/config.toml
