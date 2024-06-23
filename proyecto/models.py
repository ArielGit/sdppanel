from django.db import models

# Create your models here.

# ---------------------- MODELO ORGANISMO ------------------------------
class Organismo(models.Model):
    """Modelo para los Organismos."""
    nombre = models.CharField(max_length=360, help_text='Ingrese organismo')
    dependencia = models.CharField(max_length=360, help_text='Ingrese Dependencia de este Organismo')

    def __str__(self):
        """String for representing the Model object."""
        return self.nombre

# ---------------------- MODELO RESPONSABLE ------------------------------
class Responsable(models.Model):
    """Modelo para Respnsables del proyecto."""
    nombre = models.CharField(max_length=240, help_text='Ingrese nombre del responsable del Proyecto')
    organismo = models.ForeignKey(Organismo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.nombre

    def get_absolute_url(self):
        """Devuelve la URL para acceder a un Responsable en particular."""
        return reverse('responsable-detail', args=[str(self.id)])

# ---------------------- MODELO AREA DE INVERSION ------------------------------
class Areainversion(models.Model):
    """Modelo para las distintas areas de inversion."""
    nombre = models.CharField(max_length=200, help_text='Ingrese Area de inversion (ej.: Agricultura, Ganaderia,..)')

    def __str__(self):
        """String for representing the Model object."""
        return self.nombre

# ---------------------- MODELO LOCALIDADES ------------------------------
class Localidad(models.Model):
    """Modelo para las Localidades."""
    nombre = models.CharField(max_length=200, help_text='Ingrese Localidad (ej..)')
    departamento = models.CharField(max_length=100, help_text='Ingrese departamento)')
    latitud  = models.CharField(max_length=15, help_text='Ingrese Latitud')
    longitud = models.CharField(max_length=15, help_text='Ingrese Longitud (ej..)')

    def __str__(self):
        """String for representing the Model object."""
        return self.nombre

# ---------------------- MODELO COMUNIDAD ------------------------------
class Comunidad(models.Model):
    """Modelo para las Comunidades aborigenes."""
    nombre = models.CharField(max_length=360, help_text='Ingrese nombre de la Comunidad aborigen ')

    def __str__(self):
        """String for representing the Model object."""
        return self.nombre

# ---------------------- MODELO PROYECTO ------------------------------
from django.urls import reverse # Usado para generar URLs para reversing de URL patterns

class Proyecto(models.Model):
    """Modelo representando un PROYECTO."""
    titulo = models.CharField(max_length=250)

    # Foreign Key se usa porque proyecto puede solo tener un responsable, pero el reponsable puede tener multiples Proyectos
    responsable = models.ForeignKey(Responsable, on_delete=models.SET_NULL, null=True)

    descripcion = models.TextField(max_length=1000, help_text='Ingrese una breve descripcion del proyecto')

    # ManyToManyField se usó porque una area de inv puede tener varios proyectos. Cada proyecto puede tener varias areas de inversion.
    # La clase areainversion ya ha sido definida, por lo tanto podemos especificarla como objeto.
    areainversion = models.ManyToManyField(Areainversion, help_text='Seleccione el area de inversion para este proyecto')

    beneficiarios  = models.IntegerField()
    montoinversion  = models.IntegerField()
    anioejecucion = models.IntegerField()

    localidad = models.ForeignKey(Localidad, on_delete=models.SET_NULL, null=True)

    # Al definir un campo con OPCIONES en los Templates (html) se puede utilizar la funcion creada de forma automática
    # get_campo_display en este caso seria get_estado_proyecto_display para mostrar la descripcion en 
    # de mostrar el codigo corto.
    ESTADO_PROYECTO = (
        ('n', 'No iniciado'),
        ('e', 'En ejecucion'),
        ('t', 'Terminado'),
        ('p', 'Paralizado'),
    )

    estado = models.CharField(
        max_length=1,
        choices=ESTADO_PROYECTO,
        blank=True,
        default='e',
        help_text='Estado del proyecto',
    )


    observacion = models.TextField(max_length=1000, help_text='Ingrese una breve aclaracion')

    comunidad = models.ManyToManyField(Comunidad, help_text='Select a Comunidad aborigen para este proyecto')

    image = models.ImageField(upload_to='images/', null=True)


    def display_areainversion(self):
        """Crea un string para las areas de inversion. Esto se requiere para mostrar las Areas de inversion en Admin."""
        return ', '.join(areainversion.nombre for areainversion in self.areainversion.all()[:3])

    display_areainversion.short_description = 'Areainversion'

    def __str__(self):
        """String para la representacion del Modelo en el sitio de Administracion."""
        return self.titulo

    def get_absolute_url(self):
        """Devuelve la URL para acceder al registro de detalle para este proyecto."""
        return reverse('proyecto-detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['responsable']

# ------------------ MODELO ACTUALIZACION de data en un Proyecto ------------------
# import uuid  # Requerida para Instancias de proyectos unicos  (No usado por ahora)
from datetime import date
from django.contrib.auth.models import User  # Necesario para asignar el Usuario (User) como un editor 


class Actualizacion(models.Model):
    """Modelo para representar una Actualizacion especifica de proyecto."""
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4,
    #                      help_text="Unique ID for this particular book across whole library")
    proyecto = models.ForeignKey('Proyecto', on_delete=models.RESTRICT, null=True)
    descripcion = models.CharField(max_length=1000)
    fecha_actualizacion = models.DateField(null=True, blank=True)
    fecha_validez = models.DateField(null=True, blank=True) # Campo solo para usar de ejercicio 
    # Aqui utilizamos la variable User desde el modelo Auth 
    registrador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def es_valido(self):
        """Determina si es valido segun una fecha valida."""
        return bool(self.fecha_validez and date.today() > self.fecha_validez)

    class Meta:
        ordering = ['fecha_actualizacion']
       # permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.id, self.proyecto.titulo)


