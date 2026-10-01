import type { ColumnDef } from "@tanstack/react-table"
import { Check, Copy } from "lucide-react"

import type { StudentPublic } from "@/client"
import { Button } from "@/components/ui/button"
import { useCopyToClipboard } from "@/hooks/useCopyToClipboard"
import { StudentActionsMenu } from "./StudentActionsMenu"

function CopyId({ id }: { id: string }) {
  const [copiedText, copy] = useCopyToClipboard()
  const isCopied = copiedText === id

  return (
    <div className="flex items-center gap-1.5 group">
      <span className="font-mono text-xs text-muted-foreground">{id}</span>
      <Button
        variant="ghost"
        size="icon"
        className="size-6 opacity-0 group-hover:opacity-100 transition-opacity"
        onClick={() => copy(id)}
      >
        {isCopied ? (
          <Check className="size-3 text-green-500" />
        ) : (
          <Copy className="size-3" />
        )}
        <span className="sr-only">Copy ID</span>
      </Button>
    </div>
  )
}

export const columns: ColumnDef<StudentPublic>[] = [
  {
    accessorKey: "id",
    header: "ID",
    cell: ({ row }) => <CopyId id={row.original.id} />,
  },
  {
    accessorKey: "ien",
    header: "IEN",
    cell: ({ row }) => <span className="font-medium">{row.original.ien}</span>,
  },
  {
    accessorKey: "prenom",
    header: "Prénom",
    cell: ({ row }) => <span className="font-medium">{row.original.prenom}</span>,
  },
  {
    accessorKey: "nom",
    header: "Nom",
    cell: ({ row }) => <span className="font-medium">{row.original.nom}</span>,
  },
  {
    accessorKey: "sexe",
    header: "Sexe",
    cell: ({ row }) => <span className="font-medium">{row.original.sexe}</span>,
  },
  {
    accessorKey: "datnais",
    header: "Date de naissance",
    cell: ({ row }) => <span className="font-medium">{row.original.datnais}</span>,
  },
  {
    accessorKey: "lieunais",
    header: "Lieu de naissance",
    cell: ({ row }) => <span className="font-medium">{row.original.lieunais}</span>,
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <StudentActionsMenu student={row.original} />
      </div>
    ),
  },
]
