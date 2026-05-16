from flask import Response
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import os
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "rtsolutions-secure-secret-key-2026-advanced"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rtsolutions.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ═══════════════════════════════════════════════════════════════
# ─── DATABASE MODELS ───
# ═══════════════════════════════════════════════════════════════


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    service = db.Column(db.String(100))
    message = db.Column(db.Text)
    # new, contacted, resolved
    status = db.Column(db.String(20), default="new")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "service": self.service,
            "message": self.message,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M"),
        }


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    industry = db.Column(db.String(50))
    # active, inactive, prospect
    status = db.Column(db.String(20), default="active")
    contract_value = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "industry": self.industry,
            "status": self.status,
            "contract_value": self.contract_value,
            "notes": self.notes,
            "created_at": self.created_at.strftime("%Y-%m-%d"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d"),
        }


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100))
    role = db.Column(db.String(20), default="admin")
    theme = db.Column(db.String(20), default="professional")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    excerpt = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200))
    category = db.Column(db.String(50))
    author = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    price = db.Column(db.Float)
    features = db.Column(db.Text)


class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ═══════════════════════════════════════════════════════════════
# ─── MIDDLEWARE & DECORATORS ───
# ═══════════════════════════════════════════════════════════════


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "admin_id" not in session:
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)

    return wrapper


@app.context_processor
def inject_user():
    admin = None
    if "admin_id" in session:
        admin = Admin.query.get(session["admin_id"])
    return dict(current_admin=admin)


# ═══════════════════════════════════════════════════════════════
# ─── PUBLIC ROUTES - PAGES ───
# ═══════════════════════════════════════════════════════════════


@app.route("/")
def index():
    return render_template("pages/home.html")


@app.route("/architecture")
def architecture():
    return render_template("pages/about.html")


@app.route("/capabilities")
def capabilities():
    services = Service.query.all()
    return render_template("pages/services.html", services=services)


@app.route("/team")
def team():
    return render_template("pages/team.html")


@app.route("/features")
def features():
    return render_template("pages/features.html")


@app.route("/insights")
def insights():
    page = request.args.get("page", 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=9
    )
    return render_template("pages/blog.html", posts=posts)


@app.route("/blog/<slug>")
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug).first_or_404()
    recent_posts = (
        BlogPost.query.filter(BlogPost.id != post.id)
        .order_by(BlogPost.created_at.desc())
        .limit(3)
        .all()
    )
    return render_template(
        "pages/blog-detail.html", post=post, recent_posts=recent_posts
    )


@app.route("/faq")
def faq():
    return render_template("pages/faq.html")


@app.route("/testimonials")
def testimonials():
    testimonials = Testimonial.query.all()
    return render_template("pages/testimonials.html", testimonials=testimonials)


@app.route("/engage")
def engage():
    services_list = Service.query.all()
    return render_template("pages/contact.html", services=services_list)


@app.route("/privacy")
def privacy():
    return render_template("pages/privacy.html")


@app.route("/terms")
def terms():
    return render_template("pages/terms.html")


# ═══════════════════════════════════════════════════════════════
# ─── API ENDPOINTS - CONTACT ───
# ═══════════════════════════════════════════════════════════════


@app.route("/api/contact", methods=["POST"])
def api_contact():
    try:
        data = request.get_json()
        contact = Contact(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            company=data.get("company"),
            service=data.get("service"),
            message=data.get("message"),
        )
        db.session.add(contact)
        db.session.commit()
        return jsonify(
            {
                "status": "success",
                "message": "Thank you for reaching out! We will contact you soon.",
                "id": contact.id,
            }
        ), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/contact/list", methods=["GET"])
@admin_required
def api_contact_list():
    status_filter = request.args.get("status")
    query = Contact.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    contacts = query.order_by(Contact.created_at.desc()).all()
    return jsonify([c.to_dict() for c in contacts])


# ═══════════════════════════════════════════════════════════════
# ─── ADMIN AUTHENTICATION ───
# ═══════════════════════════════════════════════════════════════


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if "admin_id" in session:
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        data = request.get_json()
        admin = Admin.query.filter_by(username=data.get("username")).first()

        if admin and admin.check_password(data.get("password")) and admin.is_active:
            session["admin_id"] = admin.id
            session["admin_username"] = admin.username
            return jsonify(
                {"status": "success", "redirect": url_for("admin_dashboard")}
            ), 200
        return jsonify(
            {"status": "error", "message": "Invalid credentials or account disabled"}
        ), 401
    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


# ═══════════════════════════════════════════════════════════════
# ─── ADMIN DASHBOARD & MANAGEMENT ───
# ═══════════════════════════════════════════════════════════════


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    admin = Admin.query.get(session.get("admin_id"))
    stats = {
        "total_contacts": Contact.query.count(),
        "new_contacts": Contact.query.filter_by(status="new").count(),
        "contacted": Contact.query.filter_by(status="contacted").count(),
        "resolved": Contact.query.filter_by(status="resolved").count(),
        "total_clients": Client.query.count(),
        "active_clients": Client.query.filter_by(status="active").count(),
    }
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_contacts=recent_contacts,
        admin=admin,
    )


@app.route("/admin/contacts")
@admin_required
def admin_contacts():
    page = request.args.get("page", 1, type=int)
    status = request.args.get("status")
    query = Contact.query
    if status:
        query = query.filter_by(status=status)
    contacts = query.order_by(Contact.created_at.desc()).paginate(
        page=page, per_page=20
    )
    return render_template("admin/contacts.html", contacts=contacts)


@app.route("/admin/clients")
@admin_required
def admin_clients():
    page = request.args.get("page", 1, type=int)
    clients = Client.query.order_by(Client.created_at.desc()).paginate(
        page=page, per_page=20
    )
    return render_template("admin/clients.html", clients=clients)


@app.route("/admin/clients/add", methods=["GET", "POST"])
@admin_required
def admin_add_client():
    if request.method == "POST":
        try:
            data = request.get_json()
            client = Client(
                name=data.get("name"),
                email=data.get("email"),
                phone=data.get("phone"),
                company=data.get("company"),
                industry=data.get("industry"),
                status=data.get("status", "active"),
                contract_value=float(data.get("contract_value", 0)),
                notes=data.get("notes"),
            )
            db.session.add(client)
            db.session.commit()
            return jsonify({"status": "success", "id": client.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
    return render_template("admin/client-form.html")


@app.route("/admin/api/contact/<int:contact_id>", methods=["GET", "PUT", "DELETE"])
@admin_required
def manage_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)

    if request.method == "GET":
        return jsonify(contact.to_dict())

    elif request.method == "PUT":
        try:
            data = request.get_json()
            contact.status = data.get("status", contact.status)
            contact.notes = data.get("notes", contact.notes)
            db.session.commit()
            return jsonify({"status": "success", "message": "Contact updated"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

    elif request.method == "DELETE":
        try:
            db.session.delete(contact)
            db.session.commit()
            return jsonify({"status": "success", "message": "Contact deleted"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/admin/api/client/<int:client_id>", methods=["GET", "PUT", "DELETE"])
@admin_required
def manage_client(client_id):
    client = Client.query.get_or_404(client_id)

    if request.method == "GET":
        return jsonify(client.to_dict())

    elif request.method == "PUT":
        try:
            data = request.get_json()
            client.name = data.get("name", client.name)
            client.email = data.get("email", client.email)
            client.phone = data.get("phone", client.phone)
            client.company = data.get("company", client.company)
            client.industry = data.get("industry", client.industry)
            client.status = data.get("status", client.status)
            client.contract_value = float(
                data.get("contract_value", client.contract_value)
            )
            client.notes = data.get("notes", client.notes)
            db.session.commit()
            return jsonify({"status": "success", "message": "Client updated"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

    elif request.method == "DELETE":
        try:
            db.session.delete(client)
            db.session.commit()
            return jsonify({"status": "success", "message": "Client deleted"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/admin/settings")
@admin_required
def admin_settings():
    admin = Admin.query.get(session.get("admin_id"))
    return render_template("admin/settings.html", admin=admin)


@app.route("/admin/api/settings/theme", methods=["POST"])
@admin_required
def api_settings_theme():
    try:
        admin = Admin.query.get(session.get("admin_id"))
        data = request.get_json()
        admin.theme = data.get("theme", "professional")
        db.session.commit()
        return jsonify({"status": "success", "message": "Theme updated"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/admin/api/password", methods=["POST"])
@admin_required
def api_change_password():
    try:
        admin = Admin.query.get(session.get("admin_id"))
        data = request.get_json()

        if not admin.check_password(data.get("current_password")):
            return jsonify(
                {"status": "error", "message": "Current password is incorrect"}
            ), 400

        admin.set_password(data.get("new_password"))
        db.session.commit()
        return jsonify(
            {"status": "success", "message": "Password changed successfully"}
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# ─── INITIALIZATION & DATABASE ───
# ═══════════════════════════════════════════════════════════════


def init_database():
    with app.app_context():
        db.create_all()

        # Create default admin
        if Admin.query.filter_by(username="admin").first() is None:
            admin = Admin(
                username="admin",
                email="admin@rtsolutions.com",
                full_name="Administrator",
                role="admin",
                is_active=True,
            )
            admin.set_password("admin123")
            db.session.add(admin)

        # Create sample services
        if Service.query.count() == 0:
            services = [
                Service(
                    name="Web Development",
                    description="Custom web applications",
                    price=5000,
                ),
                Service(
                    name="Mobile Development",
                    description="Native and cross-platform apps",
                    price=8000,
                ),
                Service(
                    name="Cloud Solutions",
                    description="AWS and Azure deployment",
                    price=3000,
                ),
                Service(
                    name="Consulting",
                    description="Expert technical consultation",
                    price=2000,
                ),
            ]
            db.session.add_all(services)

        # Create sample testimonials
        if Testimonial.query.count() == 0:
            testimonials = [
                Testimonial(
                    author="John Smith",
                    company="Tech Innovations LLC",
                    position="CEO",
                    content="Outstanding service! They delivered exactly what we needed, on time and within budget.",
                    rating=5,
                ),
                Testimonial(
                    author="Sarah Johnson",
                    company="Digital Solutions Inc",
                    position="Project Manager",
                    content="Professional team with great communication and technical expertise.",
                    rating=5,
                ),
                Testimonial(
                    author="Michael Chen",
                    company="Enterprise Systems",
                    position="CTO",
                    content="Best decision we made for our cloud migration. Highly recommended!",
                    rating=5,
                ),
            ]
            db.session.add_all(testimonials)

        # Create sample blog posts
        if BlogPost.query.count() == 0:
            posts = [
                BlogPost(
                    title="Getting Started with Cloud Computing",
                    slug="getting-started-cloud",
                    excerpt="Learn the basics of cloud computing and why it matters for your business.",
                    content="Cloud computing has revolutionized how businesses operate...",
                    category="Cloud",
                    author="Admin",
                ),
                BlogPost(
                    title="10 Web Development Best Practices in 2026",
                    slug="web-dev-best-practices",
                    excerpt="Essential practices every web developer should follow.",
                    content="Web development continues to evolve rapidly...",
                    category="Development",
                    author="Admin",
                ),
                BlogPost(
                    title="The Future of AI in Business",
                    slug="ai-business-future",
                    excerpt="How artificial intelligence is transforming industries.",
                    content="Artificial intelligence is no longer just a buzzword...",
                    category="AI",
                    author="Admin",
                ),
            ]
            db.session.add_all(posts)

        db.session.commit()


@app.before_request
def before_request():
    if not hasattr(app, "_initialized"):
        init_database()
        app._initialized = True


@app.after_request
def add_header(response):
    if request.path.startswith("/admin") and request.endpoint != "admin_login":
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


@app.route("/sitemap.xml")
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://rtsolutions.org.in/</loc>
            <priority>1.0</priority>
        </url>
    </urlset>"""
    return Response(xml, mimetype="application/xml")


if __name__ == "__main__":
    init_database()
    app.run(debug=True, port=5000)
