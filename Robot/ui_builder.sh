# Ticket Checking UI
pyside6-uic --absolute-imports --python-paths design design/ui/ticket/checking/ticket.ui -o src/ui/ticket/checking/ticket_ui.py
pyside6-uic --absolute-imports --python-paths design design/ui/ticket/checking/result.ui -o src/ui/ticket/checking/ticket_result_ui.py
pyside6-rcc design/ui/ticket/checking/ticket.qrc -o src/ui/ticket/checking/ticket_rc.py

# User main menu
pyside6-uic --absolute-imports --python-paths design design/ui/user/main_menu.ui -o src/ui/user/main_menu_ui.py

# Auth screen
pyside6-uic --absolute-imports --python-paths design design/ui/auth/auth.ui -o src/ui/auth/auth_ui.py