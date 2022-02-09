# cs61a_fa21

tips: Add this function into Linux shell's `.*rc` file to locally run Ok autograder without add `--local` behind each
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