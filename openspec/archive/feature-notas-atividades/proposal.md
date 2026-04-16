# Change: feature-notas-atividades

## Why
Implementar funcionalidade para permitir que professores lancem notas para alunos em atividades específicas, viabilizando avaliação acadêmica com controles de acesso e propriedade.

## What Changes
- Adicionar tabelas `activity` e `activity_grade` no banco de dados.
- Criar APIs para lançamento, edição e consulta de notas.
- Garantir que somente professores donos das atividades possam gerenciar notas.
- Permitir que alunos visualizem suas próprias notas.

## Impact
- Professores ganham ferramenta para avaliação contínua.
- Alunos podem acompanhar desempenho em atividades.
- Base para futuras automações como cálculo de médias e relatórios.
- Sem impacto em funcionalidades existentes; novo módulo isolado.