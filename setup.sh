mkdir -p /app/.streamlit
echo "\
[general]\n\
email = \"m.gabr@aucegypt.edu\"\n\
" > /app/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
" > /app/.streamlit/config.toml
