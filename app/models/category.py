from datetime import datetime
from app import db
import uuid

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    
    # Phân cấp cha-con
    parent_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=True)
    
    # Metadata
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    children = db.relationship(
        'Category',
        backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def to_dict(self, include_children=False, include_parent=False):
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'image_url': self.image_url,
            'parent_id': self.parent_id,
            'sort_order': self.sort_order,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_parent and self.parent:
            data['parent'] = {
                'id': self.parent.id,
                'name': self.parent.name,
                'slug': self.parent.slug
            }
        
        if include_children:
            data['children'] = [
                child.to_dict(include_children=False) 
                for child in self.children.order_by(Category.sort_order).all()
            ]
            data['children_count'] = self.children.count()
        
        return data
    
    def get_all_children_ids(self):
        """Lấy tất cả ID của danh mục con (đệ quy)"""
        ids = [self.id]
        for child in self.children:
            ids.extend(child.get_all_children_ids())
        return ids
