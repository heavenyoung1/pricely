from src.presentation.sync_bot.handlers.delete import (
    choose_product_to_delete,
    handle_delete_product_request,
    handle_confirm_delete,
    handle_cancel_delete
)

from src.presentation.sync_bot.handlers.errors import fallback
from src.presentation.sync_bot.handlers.menu import (
    add_product_request,
    list_products,
    clear_products,
)

from src.presentation.sync_bot.handlers.navigation import (
    handle_back_to_products,
    # catch_all,
)

from src.presentation.sync_bot.handlers.products import (
    handle_product_button,
    handle_update_price,
)

from src.presentation.sync_bot.handlers.statistics import show_statistics
from src.presentation.sync_bot.handlers.start import start_handler, help_handler

