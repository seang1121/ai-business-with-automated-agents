"""Finance Agent — generates invoices after job completion."""

from datetime import datetime

from backend.agents.base_agent import BaseAgent
from backend import database as db


class FinanceAgent(BaseAgent):
    AGENT_NAME = "finance"

    def trigger(self, payload: dict) -> int | None:
        """Triggered when a job is complete and has a price_agreed."""
        job = db.get_job(payload["job_id"])
        if not job or not job.get("price_agreed"):
            return None

        lead = db.get_lead(job["lead_id"]) if job.get("lead_id") else {}
        if not lead:
            lead = {}

        # Calculate invoice
        subtotal = job["price_agreed"]
        tax_rate = self.agent_config.get("tax_rate", 0.0)
        tax = round(subtotal * tax_rate, 2)
        total = round(subtotal + tax, 2)
        invoice_number = self._next_invoice_number()

        # Store invoice in DB
        db.insert_invoice(
            job_id=job["id"],
            invoice_number=invoice_number,
            line_items=[{
                "service": job["service"],
                "price": subtotal,
            }],
            subtotal=subtotal,
            tax=tax,
            total=total,
        )

        payload["customer_name"] = lead.get("name", "Customer")
        payload["phone"] = lead.get("phone", "")
        payload["email"] = lead.get("email", "")
        payload["service"] = job["service"]
        payload["invoice_number"] = invoice_number
        payload["subtotal"] = subtotal
        payload["tax"] = tax
        payload["total"] = total
        payload["date"] = datetime.now().strftime("%B %d, %Y")
        payload["payment_methods"] = ", ".join(
            self.agent_config.get("payment_methods", ["Cash"])
        )

        return self.create_draft(payload, job_id=job["id"],
                                 lead_id=job.get("lead_id"))

    def build_prompt(self, payload: dict) -> str:
        biz = self._biz()
        return (
            f"You are the billing assistant for {biz['name']}.\n\n"
            f"Generate a professional invoice message for:\n"
            f"- Customer: {payload.get('customer_name')}\n"
            f"- Service: {payload.get('service')}\n"
            f"- Invoice #: {payload.get('invoice_number')}\n"
            f"- Subtotal: ${payload.get('subtotal', 0):.2f}\n"
            f"- Tax: ${payload.get('tax', 0):.2f}\n"
            f"- Total: ${payload.get('total', 0):.2f}\n"
            f"- Payment methods: {payload.get('payment_methods')}\n\n"
            f"Format it as a clean, professional invoice text that can be sent "
            f"via SMS or email. Include the business name and contact info. "
            f"Sign as {biz['owner_name']}."
        )

    def _next_invoice_number(self) -> str:
        prefix = self.agent_config.get("invoice_prefix", "INV")
        existing = db.get_db().execute(
            "SELECT COUNT(*) FROM invoices"
        ).fetchone()[0]
        return f"{prefix}-{existing + 1001:04d}"
