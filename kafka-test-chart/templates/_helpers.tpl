{{- define "kafka-file-log.fluentbit-sidecar" -}}
- name: fluentbit
  image: "{{ .Values.fluentbit.image.repository }}:{{ .Values.fluentbit.image.tag }}"
  imagePullPolicy: {{ .Values.fluentbit.image.pullPolicy }}
  volumeMounts:
    - name: log-volume
      mountPath: "{{ .Values.log.path }}"
    - name: config
      mountPath: /fluent-bit/etc/
  env:
    - name: FLUENT_BIT_CONFIG
      value: /fluent-bit/etc/fluent-bit.conf
  command: ["/fluent-bit/bin/fluent-bit", "-c", "/fluent-bit/etc/fluent-bit.conf"]
{{- end }}
