# cs61a_fa21

tips I learned:

1. Add this function into Linux shell's `.*rc` file to locally run Ok autograder without add `--local` behind each
   command that parsed from website:

```shell
# https://superuser.com/questions/105375/how-to-use-spaces-in-a-bash-alias-name
python3() {
    if [[ $1 == "ok" ]]; then
        command python3 ok --local ${@:2}
    else
        command python3 "$@"
    fi
}
```

2. Set `builtin.AssertError` exception breakpoint on your IDE
   ([for example on PyCharm](https://www.jetbrains.com/help/pycharm/using-breakpoints.html)), so you can easily debug by
   adding assertion between your code. It's easier than finding a proper trigger condition for normal breakpoint.