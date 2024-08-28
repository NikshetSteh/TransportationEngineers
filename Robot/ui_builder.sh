# Ticket Checking UI
pyside6-uic --absolute-imports --python-paths design design/ui/ticket/checking/ticket.ui -o src/ui/ticket/checking/ticket_ui.py
pyside6-uic --absolute-imports --python-paths design design/ui/ticket/checking/result_s.ui -o src/ui/ticket/checking/ticket_result_s_ui.py
pyside6-uic --absolute-imports --python-paths design design/ui/ticket/checking/result_f.ui -o src/ui/ticket/checking/ticket_result_f_ui.py
pyside6-rcc design/ui/ticket/checking/ticket.qrc -o src/ui/ticket/checking/ticket_rc.py
pyside6-rcc design/ui/ticket/checking/result_s.qrc -o src/ui/ticket/checking/result_s_rc.py
pyside6-rcc design/ui/ticket/checking/result_f.qrc -o src/ui/ticket/checking/result_f_rc.py

# User main menu
pyside6-uic --absolute-imports --python-paths design design/ui/user/main_menu.ui -o src/ui/user/main_menu_ui.py

# Auth screen
pyside6-uic --absolute-imports --python-paths design design/ui/auth/auth.ui -o src/ui/auth/auth_ui.py

# Destinations info list
pyside6-uic --absolute-imports --python-paths design design/ui/user/destination_info/destinations_info_list.ui -o src/ui/user/destination_info/destinations_info_list_ui.py

# Store
pyside6-uic --absolute-imports --python-paths design design/ui/store/category_selection/category_select.ui -o src/ui/store/category_selection/category_select_ui.py
pyside6-rcc design/ui/store/category_selection/category_select.qrc -o src/ui/store/category_selection/category_select_rc.py
