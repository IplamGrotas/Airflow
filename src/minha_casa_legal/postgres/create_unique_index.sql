CREATE UNIQUE INDEX IF NOT EXISTS idx_bairro_quadra_lote
ON reurb.minha_casa_legal (bairro, quadra, lote);