Statements are the building blocks of a program. Custom definition of a statement can be done by subclassing `kirin.ir.Statement`. The builtin declaration decorator `@statement` can be used to generate common statement definitions with `@dataclass`-like syntax.

::: kirin.ir.Statement
    options:
        show_root_heading: true
        merge_init_into_class: false
        group_by_category: false
        # explicit members list so we can set order and include `__init__` easily
        show_if_no_docstring: false
        members:
        - __init__
        - parent_stmt
        - parent_node
        - parent_region
        - parent_block
        - next_stmt
        - prev_stmt
        - insert_after
        - insert_before
        - replace_by
        - args
        - results
        - regions
        - successors
        - drop_all_references
        - delete
        - detach
        - from_stmt
        - walk
        - is_structurally_equal
        - print_impl
        - get_attr_or_prop
        - has_trait
        - get_trait
        - from_python_call
        - expect_one_result
        - typecheck
        - verify
