import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from reservation.models import Client, Product, Reservation, ReservationCalendar


class ClientType(DjangoObjectType):
    class Meta:
        model = Client


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class ReservationType(DjangoObjectType):
    class Meta:
        model = Reservation


class ReservationCalendarType(DjangoObjectType):
    class Meta:
        model = ReservationCalendar


class ClientInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    phone = graphene.String()
    email = graphene.String()


class ProductInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    description = graphene.String()
    price = graphene.Float()
    is_active = graphene.Boolean()


class ReservationCalendarInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    description = graphene.String()
    products = graphene.List(ProductInput)
    is_active = graphene.Boolean()


class ReservationInput(graphene.InputObjectType):
    id = graphene.ID()
    start_time = graphene.DateTime()
    end_time = graphene.DateTime()
    client = graphene.Field(ClientInput)
    calendar = graphene.Field(ReservationCalendarInput)


class Query(ObjectType):
    client = graphene.Field(ClientType, id=graphene.Int())
    product = graphene.Field(ProductType, id=graphene.Int())
    reservation = graphene.Field(ReservationType, id=graphene.Int())
    calendar = graphene.Field(ReservationCalendarType, id=graphene.Int())
    clients = graphene.List(ClientType)
    products = graphene.List(ProductType)
    reservations = graphene.List(ReservationType)
    calendars = graphene.List(ReservationCalendarType)

    def resolve_client(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Client.objects.get(pk=id)
        return None

    def resolve_product(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Product.objects.get(pk=id)
        return None

    def resolve_reservation(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Reservation.objects.get(pk=id)
        return None

    def resolve_calendar(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return ReservationCalendar.objects.get(pk=id)
        return None

    def resolve_clients(self, info, **kwargs):
        return Client.objects.all()

    def resolve_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_reservations(self, info, **kwargs):
        return Reservation.objects.all()

    def resolve_calendars(self, info, **kwargs):
        return ReservationCalendar.objects.all()


class CreateClient(graphene.Mutation):
    class Arguments:
        input = ClientInput(required=True)
    ok = graphene.Boolean()
    client = graphene.Field(ClientType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        client_instance = Client(
            name=input.name,
            phone=input.phone,
            email=input.email
        )
        client_instance.save()
        return CreateClient(ok=ok, client=client_instance)


class UpdateClient(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ClientInput(required=True)
    ok = graphene.Boolean()
    client = graphene.Field(ClientType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        client_instance = Client.objects.get(pk=id)
        if client_instance:
            ok = True
            client_instance.name = input.name
            client_instance.phone = input.phone
            client_instance.email = input.email
            client_instance.save()
            return UpdateClient(ok=ok, client=client_instance)
        return UpdateClient(ok=ok, client=None)


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)
    ok = graphene.Boolean()
    product = graphene.Field(ProductType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        product_instance = Product(
            name=input.name,
            description=input.description,
            price=input.price,
            is_active=input.is_active
        )
        product_instance.save()
        return CreateProduct(ok=ok, product=product_instance)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ProductInput(required=True)
    ok = graphene.Boolean()
    product = graphene.Field(ProductType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        product_instance = Product.objects.get(pk=id)
        if product_instance:
            ok = True
            product_instance.name = input.name
            product_instance.description = input.description
            product_instance.price = input.price
            product_instance.is_active = input.is_active
            product_instance.save()
            return UpdateProduct(ok=ok, product=product_instance)
        return UpdateProduct(ok=ok, product=None)

class CreateReservation(graphene.Mutation):
    class Arguments:
        input = ReservationInput(required=True)
    ok = graphene.Boolean()
    reservation = graphene.Field(ReservationType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        reservation_instance = Reservation(
            start_time = input.start_time,
            end_time = input.end_time,
            client = input.client, # TODO: create new client or assign existing
            calendar = input.calendar # TODO: create new calendar or assign existing
        )
        reservation_instance.save()
        return CreateReservation(ok=ok, reservation=reservation_instance)


class Mutation(graphene.ObjectType):
    create_client = CreateClient.Field()
    update_client = UpdateClient.Field()
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    create_reservation = CreateReservation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
