from src.presentation.bot.handlers.delete import (
    choose_product_to_delete,
    handle_delete_product_request,
    handle_confirm_delete,
    handle_cancel_delete
)

from src.presentation.bot.handlers.errors import fallback
from src.presentation.bot.handlers.menu import (
    add_product_request,
    list_products,
    clear_products,
)

from src.presentation.bot.handlers.navigation import (
    handle_back_to_products,
    catch_all,
)

from src.presentation.bot.handlers.products import (
    handle_product_button,
    handle_update_price,
)

from src.presentation.bot.handlers.statistics import show_statistics
from src.presentation.bot.handlers.start import start_handler, help_handler

