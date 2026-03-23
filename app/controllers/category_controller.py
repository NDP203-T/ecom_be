from app.services.category_service import CategoryService
from app.services.cloudinary_service import CloudinaryService
import logging
import re

logger = logging.getLogger(__name__)

class CategoryController:
    
    @staticmethod
    def get_all_categories(include_children=False, only_parents=False, is_active=None):
        """Lấy danh sách danh mục"""
        categories = CategoryService.get_all_categories(only_parents, is_active)
        
        return {
            'categories': [cat.to_dict(include_children=include_children) for cat in categories],
            'total': len(categories)
        }, 200
    
    @staticmethod
    def get_category_tree():
        """Lấy cây danh mục phân cấp"""
        tree = CategoryService.get_category_tree()
        
        return {
            'categories': tree
        }, 200
    
    @staticmethod
    def get_category_by_id(category_id, include_children=True):
        """Lấy chi tiết danh mục theo ID"""
        category = CategoryService.get_category_by_id(category_id)
        
        if not category:
            return {'error': 'Category not found'}, 404
        
        return {
            'category': category.to_dict(include_children=include_children, include_parent=True)
        }, 200
    
    @staticmethod
    def get_category_by_slug(slug, include_children=True):
        """Lấy danh mục theo slug"""
        category = CategoryService.get_category_by_slug(slug)
        
        if not category:
            return {'error': 'Category not found'}, 404
        
        return {
            'category': category.to_dict(include_children=include_children, include_parent=True)
        }, 200
    
    @staticmethod
    def create_category(data):
        """Tạo danh mục mới"""
        # Validate slug format (chỉ cho phép chữ thường, số, dấu gạch ngang)
        slug = data['slug'].lower().strip()
        if not re.match(r'^[a-z0-9-]+$', slug):
            return {'error': 'Slug must contain only lowercase letters, numbers, and hyphens'}, 400
        
        # Check slug uniqueness
        if CategoryService.get_category_by_slug(slug):
            return {'error': 'Slug already exists'}, 400
        
        # Validate parent_id if provided
        if data.get('parent_id'):
            parent = CategoryService.get_category_by_id(data['parent_id'])
            if not parent:
                return {'error': 'Parent category not found'}, 404
        
        category = CategoryService.create_category(data)
        
        logger.info(f"Category created: {category.id} - {category.name}")
        
        return {
            'message': 'Category created successfully',
            'category': category.to_dict(include_children=True)
        }, 201
    
    @staticmethod
    def update_category(category_id, data):
        """Cập nhật danh mục"""
        category = CategoryService.get_category_by_id(category_id)
        
        if not category:
            return {'error': 'Category not found'}, 404
        
        # Validate slug if changed
        if 'slug' in data:
            slug = data['slug'].lower().strip()
            if not re.match(r'^[a-z0-9-]+$', slug):
                return {'error': 'Slug must contain only lowercase letters, numbers, and hyphens'}, 400
            
            if slug != category.slug:
                existing = CategoryService.get_category_by_slug(slug)
                if existing:
                    return {'error': 'Slug already exists'}, 400
        
        # Validate parent_id if changed
        if 'parent_id' in data:
            # Không cho phép set parent là chính nó
            if data['parent_id'] == category_id:
                return {'error': 'Category cannot be its own parent'}, 400
            
            # Không cho phép set parent là con của nó (tránh vòng lặp)
            if data['parent_id']:
                parent = CategoryService.get_category_by_id(data['parent_id'])
                if not parent:
                    return {'error': 'Parent category not found'}, 404
                
                # Check if new parent is a child of current category
                all_children_ids = category.get_all_children_ids()
                if data['parent_id'] in all_children_ids:
                    return {'error': 'Cannot set a child category as parent (circular reference)'}, 400
        
        updated_category = CategoryService.update_category(category_id, data)
        
        logger.info(f"Category updated: {category_id}")
        
        return {
            'message': 'Category updated successfully',
            'category': updated_category.to_dict(include_children=True)
        }, 200
    
    @staticmethod
    def delete_category(category_id):
        """Xóa danh mục"""
        category = CategoryService.get_category_by_id(category_id)
        
        if not category:
            return {'error': 'Category not found'}, 404
        
        # Check if category has children
        if category.children.count() > 0:
            return {
                'error': 'Cannot delete category with children. Please delete or reassign children first.'
            }, 400
        
        # Xóa ảnh trên Cloudinary nếu có
        if category.image_url:
            CloudinaryService.delete_image_from_url(category.image_url)
        
        CategoryService.delete_category(category_id)
        
        logger.info(f"Category deleted: {category_id}")
        
        return {'message': 'Category deleted successfully'}, 200
    
    @staticmethod
    def toggle_category_status(category_id):
        """Ẩn/hiện danh mục"""
        category = CategoryService.get_category_by_id(category_id)
        
        if not category:
            return {'error': 'Category not found'}, 404
        
        new_status = CategoryService.toggle_category_status(category_id)
        
        return {
            'message': f'Category {"activated" if new_status else "deactivated"} successfully',
            'category': category.to_dict()
        }, 200
