import os

import reflex as rx

# Visit logging writes SQLite files under data/. Granian ignores *.db but not
# WAL sidecar files (*.db-wal, *.db-shm), which would restart the app on every
# page load. A relative path is required: Windows drive letters contain ":".
os.environ.setdefault("REFLEX_HOT_RELOAD_EXCLUDE_PATHS", "data")

config = rx.Config(
    app_name="app",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
