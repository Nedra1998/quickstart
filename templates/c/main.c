int main(int argc, char *argv[])
{
{% props.git=true %}
    printf("Git URL: %s\n", "{{ props.git_url }}");
{% end %}
    return 0;
}
