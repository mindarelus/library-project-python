import os

# DAO
from dao.idgen_uuid import IdGenUuid
from dao.user_repository_jsonfile import UserRepositoryJsonFile
from dao.book_repository_jsonfile import BookRepositoryJsonFile
from dao.purchase_repository_jsonfile import PurchaseRepositoryJsonFile

# Services
from services.auth_service import AuthService
from services.book_service import BookService
from services.billing_service import BillingService
from services.admin_service import AdminService
from services.config_service import ConfigService

# Views
from view.guest_view import GuestView
from view.reader_view import ReaderView
from view.author_view import AuthorView
from view.book_view import BookView
from view.admin_view import AdminView

# Controller
from controller.app_controller import AppController

# --- Main Application Entry Point ---

if __name__ == '__main__':
    # --- Initialization ---
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('books'):
        os.makedirs('books')

    # Setup repositories
    uuid_generator = IdGenUuid()
    user_repo = UserRepositoryJsonFile('data/users.json', uuid_generator)
    book_repo = BookRepositoryJsonFile('data/books.json', uuid_generator)
    purchase_repo = PurchaseRepositoryJsonFile('data/purchases.json', uuid_generator)

    # Setup services
    config_service = ConfigService()
    auth_service = AuthService(user_repo)
    book_service = BookService(book_repo, user_repo, purchase_repo, config_service)
    billing_service = BillingService(user_repo, book_repo, purchase_repo)
    admin_service = AdminService(user_repo)

    # Setup views
    guest_view = GuestView()
    reader_view = ReaderView()
    author_view = AuthorView()
    book_view = BookView(billing_service)
    admin_view = AdminView()

    # Setup controller
    app_controller = AppController(
        auth_service, book_service, billing_service, admin_service, config_service,
        guest_view, reader_view, author_view, book_view, admin_view
    )

    # Create a default admin if one doesn't exist
    if not user_repo.find_by_email('admin@library.com'):
        auth_service.register_user('Admin', 'admin@library.com', 'admin123', 'admin')
        print("Default admin user 'admin@library.com' with password 'admin123' created.")

    # --- Main Application Loop ---
    while True:
        current_user = auth_service.get_current_user()
        if not current_user:
            if app_controller.run_guest_flow() == "exit":
                break
        elif current_user.role == 'reader':
            app_controller.run_reader_flow()
        elif current_user.role == 'author':
            app_controller.run_author_flow()
        elif current_user.role == 'admin':
            app_controller.run_admin_flow()
    
    print("\nThank you for using the Library App!")
