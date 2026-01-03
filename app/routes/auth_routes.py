"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)
auth_controller = AuthController()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if request.method == 'GET':
        if auth_controller.is_authenticated():
            user = auth_controller.get_current_user()
            return redirect(auth_controller._get_role_dashboard(user['role']))
        return render_template('auth/login.html')
    
    # POST request
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Username and password required'}), 400
        return render_template('auth/login.html', error='Username and password required')
    
    result = auth_controller.login(username, password)
    
    if request.is_json:
        if result['success']:
            return jsonify(result), 200
        return jsonify(result), 401
    
    if result['success']:
        return redirect(result['redirect'])
    return render_template('auth/login.html', error=result['message'])

@auth_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    """Logout route"""
    result = auth_controller.logout()
    if request.is_json:
        return jsonify(result), 200
    return redirect(url_for('auth.login'))

@auth_bp.route('/api/current-user', methods=['GET'])
def get_current_user():
    """Get current user API"""
    user = auth_controller.get_current_user()
    if user:
        return jsonify({'success': True, 'data': user}), 200
    return jsonify({'success': False, 'message': 'Not authenticated'}), 401

