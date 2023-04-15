mkdir -p /app/.streamlit
echo "\
[general]\n\
<<<<<<< HEAD
email = \"your-email@domain.com\"\n\
=======
email = \"m.gabr@aucegypt.edu\"\n\
>>>>>>> origin/main
" > /app/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
" > /app/.streamlit/config.toml
