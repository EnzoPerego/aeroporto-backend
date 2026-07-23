"""Popula o banco com dados de exemplo para facilitar testes manuais.

Uso: python -m app.seed
"""
from datetime import datetime, timedelta

from app import models
from app.database import Base, SessionLocal, engine


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(models.Terminal).first():
            print("Banco já contém dados, seed ignorado.")
            return

        t1 = models.Terminal(nome="Terminal 1", tipo="nacional")
        t2 = models.Terminal(nome="Terminal 2", tipo="internacional")
        db.add_all([t1, t2])
        db.flush()

        g1 = models.Gate(codigo="A1", terminal_id=t1.id)
        g2 = models.Gate(codigo="A2", terminal_id=t1.id)
        g3 = models.Gate(codigo="B1", terminal_id=t2.id)
        db.add_all([g1, g2, g3])
        db.flush()

        a1 = models.Aeronave(modelo="Airbus A320", matricula="PR-ABC", capacidade_maxima=180)
        a2 = models.Aeronave(modelo="Boeing 787", matricula="PR-XYZ", capacidade_maxima=250)
        db.add_all([a1, a2])
        db.flush()

        agora = datetime.utcnow()
        v1 = models.Voo(
            numero_voo="CT101",
            origem="Cape Town",
            destino="Johannesburg",
            horario_previsto_chegada=agora + timedelta(hours=2),
            horario_previsto_partida=agora + timedelta(hours=3),
            aeronave_id=a1.id,
            terminal_id=t1.id,
            gate_id=g1.id,
        )
        v2 = models.Voo(
            numero_voo="CT202",
            origem="Cape Town",
            destino="London",
            horario_previsto_chegada=agora + timedelta(hours=4),
            horario_previsto_partida=agora + timedelta(hours=5),
            aeronave_id=a2.id,
            terminal_id=t2.id,
            gate_id=g3.id,
        )
        db.add_all([v1, v2])
        db.flush()

        p1 = models.Passageiro(nome="Ana Silva", documento="11111111111", email="ana@example.com")
        p2 = models.Passageiro(nome="Bruno Costa", documento="22222222222", email="bruno@example.com")
        db.add_all([p1, p2])
        db.flush()

        r1 = models.Reserva(passageiro_id=p1.id, voo_id=v1.id, assento="12A")
        r2 = models.Reserva(passageiro_id=p2.id, voo_id=v1.id, assento="12B")
        db.add_all([r1, r2])
        db.flush()

        m1 = models.Mala(codigo_identificacao="BAG-0001", reserva_id=r1.id, localizacao_atual="Terminal 1 - Triagem")
        m2 = models.Mala(codigo_identificacao="BAG-0002", reserva_id=r2.id, localizacao_atual="Terminal 1 - Triagem")
        db.add_all([m1, m2])

        db.commit()
        print("Seed concluído com sucesso.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
