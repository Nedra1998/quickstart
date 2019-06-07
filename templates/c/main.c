int main(int argc, char *argv[])
{
{% props.git=true %}
    printf("Git URL: %s\n", "{{ props.git_url }}");
{% props.tools=true&&props.TOOLS.CI=true %}
    printf("Using %s\n", "{{ props.TOOLS.CI_SERVICE }}");
{% end %}
{% end %}
    return 0;
}
