#include <QObject>
#include <QJsonObject>
#include <QMetaObject>
#include <QMetaProperty>
#include <QMetaMethod>
#include <QJsonValue>

#define READ_WRITE_VALUE(_type,val) 		\
_type get_##val() const {return val;}			\
void set_##val(const _type& _t){val = _t;}

#define READ_WRITE_VALUE_TEMPLATE(val) \
auto get_##val() const -> decltype(val) { return val; } \
void set_##val(const decltype(val)& _t) { val = _t; }

#define READ_FUNC_NAME(_name) 	get_##_name
#define WRITE_FUNC_NAME(_name) 	set_##_name

#define READ_OBJECT(_name)	Q_INVOKABLE QJsonObject read_##_name(){return objDump(&_name);}

#define WRITE_OBJECT(_name)	Q_INVOKABLE void set_##_name(const QJsonObject& _jsonObj){ objLoad(_jsonObj,&_name);}

inline QJsonObject objDump(QObject* _obj)
{
    QJsonObject _jsonObj;

    auto _meatObj = _obj->metaObject();

    for(int i = _meatObj->propertyOffset(); i < _meatObj->propertyCount(); i++)
    {
        auto _property = _meatObj->property(i);
        auto _type = _property.type();
        if(_type < QVariant::UserType)
        {
            _jsonObj[_property.name()] = _property.read(_obj).toJsonValue();
        }
    }

    for(int i = _meatObj->methodOffset(); i < _meatObj->methodCount(); i++)
    {
        auto _meth = _meatObj->method(i);
        if(_meth.returnType() != QMetaType::QJsonObject)
        {
            continue;
        }

        QJsonObject _tempObj;
        _meth.invoke(_obj,Qt::AutoConnection,Q_RETURN_ARG(QJsonObject,_tempObj));

        QString _key = _meth.name();
        _key = _key.remove("read_");
        _jsonObj[_key] = _tempObj;
    }

    return _jsonObj;
}

inline void objLoad(const QJsonObject& jsonObj,QObject* _obj)
{
    auto _meatObj = _obj->metaObject();

    for(int i = _meatObj->propertyOffset(); i < _meatObj->propertyCount(); i++)
    {
        auto _property = _meatObj->property(i);
        QJsonValue _val = jsonObj[_property.name()];
        _property.write(_obj,_val.toVariant());
    }

    for(int i = _meatObj->methodOffset(); i < _meatObj->methodCount(); i++)
    {
        auto _meth = _meatObj->method(i);
        if(_meth.returnType() != QMetaType::Void)
        {
            continue;
        }

        QString _key = _meth.name();
        _key = _key.remove("set_");
        QJsonObject tempObj = jsonObj[_key].toObject();
        _meth.invoke(_obj,Q_ARG(QJsonObject,tempObj));

    }
}