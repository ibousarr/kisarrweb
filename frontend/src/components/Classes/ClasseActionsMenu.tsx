import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { ClassePublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import DeleteClasse from "../Classes/DeleteClasse"
import EditClasse from "../Classes/EditClasse"

interface ClasseActionsMenuProps {
  classe: ClassePublic
}

export const ClasseActionsMenu = ({ classe }: ClasseActionsMenuProps) => {
  const [open, setOpen] = useState(false)

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <EllipsisVertical />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <EditClasse classe={classe} onSuccess={() => setOpen(false)} />
        <DeleteClasse id={classe.id} onSuccess={() => setOpen(false)} />
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
