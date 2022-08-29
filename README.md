# ksym_gpl
`ksym_gpl` is a library dedicated to tracking with android kernel
symbols are gpl and which are not. The reasoning for this is
that the android release kernel combines the two sections into
one, making it hard to know the different bounds, and therefore
which symbol is which.