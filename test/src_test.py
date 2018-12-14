from bin.shell import shell, check_shell_lines


def src_common_test():
    return shell('x src common')


def src_diff_test():
    return check_shell_lines('x src diff', 3000, 4000)


def src_list_test():
    return shell('x src list')


def src_base_test():
    return shell('x src base')


def src_missing_test():
    return shell('x src missing')


def src_unique_test():
    return shell('x src unique')


def src_changed_test():
    return shell('x src changed')


def src_same_test():
    return shell('x src same')


