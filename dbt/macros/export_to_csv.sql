{% macro export_csv(model_name, output_path) %}
    {% set query %}
        select * from {{ ref(model_name) }}
    {% endset %}

    {% set results = run_query(query) %}

    {% if execute %}
        {% set df = results.to_dataframe() %}
        {{ log("Exporting " ~ model_name ~ " to " ~ output_path, info=True) }}
        {{ return(df.to_csv(output_path, index=False)) }}
    {% endif %}
{% endmacro %}
