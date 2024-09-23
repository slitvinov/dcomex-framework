{
    sub(/;.*/, "")
}

/range/ {
    name = $2
    sub(/.*range:?/, "")
    sub(/}.*/, "")
    printf "(\"%s\", \"rnd\", %s, %s),\n", name, $1, $3
    next
}

{
    name = $2
    val = $4
    if (val == "true" || val == "false")
	val = "\"" val "\""
    printf "(\"%s\", \"fix\", %s),\n", name, val
}
