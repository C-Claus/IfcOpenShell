#include "mapping_undefine.i"
#define CURVE(T) \
	if (l->as<IfcSchema::T>()) return convert(l->as<IfcSchema::T>(), r);
#include "mapping_define_missing.i"

#include "mapping.i"