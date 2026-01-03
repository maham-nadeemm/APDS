"""
Flask Application Factory
"""
from flask import Flask
from app.database import init_db

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.api_routes import api_bp
    from app.routes.form_routes import forms_bp
    from app.routes.view_routes import views_bp
    from app.routes.report_routes import reports_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(forms_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(reports_bp)
    
    # Root route
    @app.route('/')
    def index():
        from flask import redirect, url_for
        from app.controllers.auth_controller import AuthController
        auth_controller = AuthController()
        if auth_controller.is_authenticated():
            user = auth_controller.get_current_user()
            return redirect(auth_controller._get_role_dashboard(user['role']))
        return redirect(url_for('auth.login'))
    
    return app
