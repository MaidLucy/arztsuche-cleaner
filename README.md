# What this is

I spent about 120 minutes to learn enough about `jq` to write this filter,
so that I can use the [Arzt-Suche API](https://arztsuche.116117.de/) more efficiently.

# How to use

1. Obtain a working request.
You can use the development view of your browser to copy a working request as a `curl`

2. Pipe this into `jq`. e.g.:
```bash
curl -X POST ……… | jq -f filter.jq
```

You can also of course just pipe a downloaded json-file into it.
