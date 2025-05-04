# Notas para usar terraform

```bash
# Para bajar elas dependecnias, osea el provider
terraform init
# validar el codigo tf
terraform validate
# Ver que cambios se van a aplicar
terraform plan -out=plan.tfplan
# Aplicar dichos cambios
terraform apply plan.tfplan
# Imprimir las outputs, si aplica
terraform output -json > ../output.json
# Destruir la infraestructura asociada a este codigo
terraform destroy
```

Existe la opcion de usar terraform en contenedor pero supongo que se necesita unir con un volumen el directorio de trabajo

```bash
docker run hashicorp/terraform init
```
