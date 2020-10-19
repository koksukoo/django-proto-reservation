import graphene
import reservation.schema

class Query(reservation.schema.Query, graphene.ObjectType):
    pass

class Mutation(reservation.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)