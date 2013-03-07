## ArrayField

## Integration with South

The `ArrayField`s can be used with South. To enable that you need to add the
following three lines.

    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^djangopg\.fields\.TextArrayField"])
    add_introspection_rules([], ["^djangopg\.fields\.IntArrayField"])


## Indexes

You have to use a GIN index for the array column.

For instance,

    CREATE INDEX array_idx ON table USING GIN(column)
