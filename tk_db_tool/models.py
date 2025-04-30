from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class SqlAlChemyBase(DeclarativeBase):
    pass

    def set_special_fields(self, special_fields: list[str]  = None):
        self.special_fields = special_fields or []

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in self.special_fields}

    def _parse_datetime(self, time_str):
        """统一处理时间格式转换"""
        if not time_str:
            return None
        try:
            # 处理可能的格式: "2023-10-2316:09:47" 或 "2023-10-23 16:09:47"
            time_str = str(time_str).replace(' ', '')
            return datetime.strptime(time_str, '%Y-%m-%d%H:%M:%S')
        except ValueError as e:
            print(f"时间格式解析错误: {time_str}, 错误: {str(e)}")
            return None
    def set_mapping_fields(self, mapping_fields: dict):
        """设置映射字段"""
        self.mapping_fields = mapping_fields or None
    
    def set_obj_by_dict(self, obj_dict: dict):
        """设置对象属性"""
        if self.mapping_fields is None:
            raise ValueError("mapping_fields未设置")
        for obj_field, (attr_name, field_type, required) in self.mapping_fields.items():
            raw_value = obj_dict.get(obj_field)
            
            # 处理 null 值
            value = None if isinstance(raw_value, str) and raw_value.lower() == 'null' else raw_value
            
            # 必填字段检查
            if required and value is None:
                raise ValueError(f"必填字段缺失: {obj_field}")
            
            # 类型转换
            if value is not None:
                try:
                    if field_type == 'int':
                        # 检查是否是浮点数
                        if  '.' in str(value):
                            raise  ValueError(f"字段[{obj_field}]类型错误: {field_type},值: {[value]}")
                        #  检查是否是数字
                        if not str(value).strip().isdigit():
                            raise  ValueError(f"字段[{obj_field}]类型错误: {field_type},值: {[value]}")
                        value = int(value)
                    elif field_type == 'datetime':
                        value = self._parse_datetime(value)
                    elif field_type == 'str':
                        value = str(value).strip() if value else ''
                    elif field_type == 'float':
                        value = float(value)
                except (ValueError, TypeError, AttributeError) as e:
                    print(f"字段[{obj_field}]转换错误: {str(e)}")
                    value = None
            
            setattr(self, attr_name, value)
