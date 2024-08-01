# Ticket Checking UI
pyside6-uic --absolute-imports --python-paths design design/ui/ticket/checking/ticket.ui -o src/ui/ticket/checking/ticket_ui.py
pyside6-uic --absolute-imports --python-paths design design/ui/ticket/checking/result.ui -o src/ui/ticket/checking/ticket_result_ui.py
pyside6-rcc design/ui/ticket/checking/ticket.qrc -o src/ui/ticket/checking/ticket_rc.py