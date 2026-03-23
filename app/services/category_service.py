from app import db
from app.models.category import Category

class CategoryService:
    
    @staticmethod
    def get_all_categories(only_parents=False, is_active=None):
        """Lấy danh sách danh mục"""
        query = Category.query
        
        if only_parents:
            query = query.filter_by(parent_id=None)
        
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true' if isinstance(is_active, str) else is_active
            query = query.filter_by(is_active=is_active_bool)
        
        return query.order_by(Category.sort_order, Category.name).all()
    
    @staticmethod
    def get_category_tree():
        """Lấy cây danh mục phân cấp"""
        # Lấy tất cả danh mục cha (không có parent)
        root_categories = Category.query.filter_by(parent_id=None).order_by(
            Category.sort_order, Category.name
        ).all()
        
        return [cat.to_dict(include_children=True) for cat in root_categories]
    
    @staticmethod
    def get_category_by_id(category_id):
        """Lấy danh mục theo ID"""
        return Category.query.get(category_id)
    
    @staticmethod
    def get_category_by_slug(slug):
        """Lấy danh mục theo slug"""
        return Category.query.filter_by(slug=slug.lower()).first()
    
    @staticmethod
    def create_category(data):
        """Tạo danh mục mới"""
        category = Category(
            name=data['name'],
            slug=data['slug'].lower(),
            description=data.get('description'),
            image_url=data.get('image_url'),
            parent_id=data.get('parent_id'),
            sort_order=data.get('sort_order', 0),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(category)
        db.session.commit()
        
        return category
    
    @staticmethod
    def update_category(category_id, data):
        """Cập nhật danh mục"""
        category = Category.query.get(category_id)
        
        if category:
            for key, value in data.items():
                if hasattr(category, key):
                    if key == 'slug':
                        value = value.lower()
                    setattr(category, key, value)
            
            db.session.commit()
        
        return category
    
    @staticmethod
    def delete_category(category_id):
        """Xóa danh mục"""
        category = Category.query.get(category_id)
        
        if category:
            db.session.delete(category)
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def toggle_category_status(category_id):
        """Ẩn/hiện danh mục"""
        category = Category.query.get(category_id)
        
        if category:
            category.is_active = not category.is_active
            db.session.commit()
            return category.is_active
        
        return None
