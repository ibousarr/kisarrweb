import type { ColumnDef } from "@tanstack/react-table"
import { Check, Copy } from "lucide-react"

import type { SchoolPublic } from "@/client"
import { Button } from "@/components/ui/button"
import { useCopyToClipboard } from "@/hooks/useCopyToClipboard"
import { cn } from "@/lib/utils"
import { SchoolActionsMenu } from "./SchoolActionsMenu"

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

export const columns: ColumnDef<SchoolPublic>[] = [
  {
    accessorKey: "id",
    header: "ID",
    cell: ({ row }) => <CopyId id={row.original.id} />,
  },
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => <span className="font-medium">{row.original.name}</span>,
  },
  {
    accessorKey: "academie",
    header: "Académie",
    cell: ({ row }) => {
      const academie = row.original.academie
      return (
        <span
          className={cn(
            "max-w-xs truncate block text-muted-foreground",
            !academie && "italic",
          )}
        >
          {academie || "No academie"}
        </span>
      )
    },
  },
  {
    accessorKey: "ief",
    header: "IEF",
    cell: ({ row }) => {
      const ief = row.original.ief
      return (
        <span
          className={cn(
            "max-w-xs truncate block text-muted-foreground",
            !ief && "italic",
          )}
        >
          {ief || "No ief"}
        </span>
      )
    },
  },
  {
    accessorKey: "directeur",
    header: "C.E.",
    cell: ({ row }) => {
      const directeur = row.original.directeur
      return (
        <span
          className={cn(
            "max-w-xs truncate block text-muted-foreground",
            !directeur && "italic",
          )}
        >
          {directeur || "No directeur"}
        </span>
      )
    },
  },
  {
    accessorKey: "email",
    header: "Email",
    cell: ({ row }) => {
      const email = row.original.email
      return (
        <span
          className={cn(
            "max-w-xs truncate block text-muted-foreground",
            !email && "italic",
          )}
        >
          {email || "No email"}
        </span>
      )
    },
  },
  {
    accessorKey: "phone",
    header: "Téléphone",
    cell: ({ row }) => {
      const phone = row.original.phone
      return (
        <span
          className={cn(
            "max-w-xs truncate block text-muted-foreground",
            !phone && "italic",
          )}
        >
          {phone || "No phone"}
        </span>
      )
    },
  },
  {
    accessorKey: "adresse",
    header: "Adresse",
    cell: ({ row }) => {
      const adresse = row.original.adresse
      return (
        <span
          className={cn(
            "max-w-xs truncate block text-muted-foreground",
            !adresse && "italic",
          )}
        >
          {adresse || "No adresse"}
        </span>
      )
    },
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <SchoolActionsMenu school={row.original} />
      </div>
    ),
  },
]
