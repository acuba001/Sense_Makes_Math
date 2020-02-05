from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from flask import current_app, url_for
from hashlib import md5
from flask_login import UserMixin, AnonymousUserMixin
from app import db


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(UserMixin, PaginatedAPIMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    avatar_hash = db.Column(db.String(32))
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'),
                        nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()
            if self.email == current_app.config['ADMIN_CONTACT']:
                self.role = Role.query.filter_by(name='Administrator').first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def get_token(self, expires_in=3600):
    #     now = datetime.utcnow()
    #     if self.token and self.token_expiration > now + timedelta(seconds=60):
    #         return self.token
    #     self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
    #     self.token_expiration = now + timedelta(seconds=expires_in)
    #     db.session.add(self)
    #     return self.token

    # def revoke_token(self):
    #     self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    # @staticmethod
    # def check_token(token):
    #     user = User.query.filter_by(token=token).first()
    #     if user is None or user.token_expiration < datetime.utcnow():
    #         return None
    #     return user

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() + 'Z',
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'url': url_for('api.get_user', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.password = data['password']

    def gravatar_hash(self):
        return md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy=True)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id),
        }
        return json_comment

    @staticmethod
    def from_dict(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise Exception('comment does not have a body')
        return Comment(body=body)


class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer)
    resource_type = db.Column(db.Text)
    channel_id = db.Column(db.Integer)
    player_html = db.Column(db.Text)

    def to_dict(self):
        json_video_resource = {
            "resource_id": self.id,
            "resource_type": self.resource_type,  # "youtube#playlist",
            "channel_id": self.channel_id,
            "player": {
                "embedHtml": self.player_html
            }
        }
        return json_video_resource

    @staticmethod
    def from_dict(video_resource):
        if not isinstance(object, video_resource):
            if not set(('resource_id', 'resource_type')) <= set(video_resource.dict_keys):
                raise Exception('Invalid fields')
            else:
                raise Exception('Invalid Type')
        return Video(
            resource_id=video_resource['resource_id'],
            resource_type=video_resource['resource_type']
        )
