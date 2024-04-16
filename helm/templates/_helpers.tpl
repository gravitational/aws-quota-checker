{{/*
Expand the name of the chart.
*/}}
{{- define "aws-quota-checker.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "aws-quota-checker.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "aws-quota-checker.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "aws-quota-checker.commonLabels" -}}
helm.sh/chart: {{ include "aws-quota-checker.chart" . }}
{{ include "aws-quota-checker.selectorCommonLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "aws-quota-checker.selectorCommonLabels" -}}
app.kubernetes.io/name: {{ include "aws-quota-checker.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Dashboards to deploy
*/}}
{{- define "aws-quota-checker.enabledDashboardsYaml" -}}
{{- $filteredFiles := dict }}
{{- range $fileName, $fileContent := .Files.Glob "grafana-dashboards/*.json" }}
{{- $baseFileName := base $fileName }}
{{- if not (has $baseFileName $.Values.dashboards.ignoredDashboards) }}
{{- $_ := set $filteredFiles $baseFileName ($fileContent | toString) }}
{{- end }}
{{- end }}
{{- $filteredFiles | toYaml }}
{{- end }}