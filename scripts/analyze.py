#!/usr/bin/env python
"""
Script d'analyse automatisée de sécurité et qualité pour Librairie ABC.

Utilise:
- pylint : Analyse de qualité globale
- flake8 : Vérification de style PEP 8
- bandit : Analyse de sécurité
- coverage : Couverture des tests

Exécution:
    python scripts/analyze.py
"""

import subprocess
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple
import re


class CodeAnalyzer:
    """Analyste de code qui centralise les outils d'analyse."""

    def __init__(self, root_dir: str = "."):
        """Initialise l'analyseur."""
        self.root_dir = Path(root_dir)
        self.src_dir = self.root_dir / "src"
        self.tests_dir = self.root_dir / "tests"
        self.reports_dir = self.root_dir / "reports"
        self.reports_dir.mkdir(exist_ok=True)

        self.results = {
            "pylint": None,
            "flake8": None,
            "bandit": None,
            "coverage": None,
            "summary": {}
        }

    def run_pylint(self) -> Dict:
        """Exécute pylint sur le code source."""
        print("\n" + "=" * 60)
        print("🔍 PYLINT - Analyse de qualité")
        print("=" * 60)

        try:
            cmd = [
                "pylint",
                "--rcfile=.pylintrc",
                f"--output-format=json",
                f"--reports=n",
                str(self.src_dir),
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.root_dir
            )

            try:
                messages = json.loads(result.stdout) if result.stdout else []
            except json.JSONDecodeError:
                messages = []

            # Compter les problèmes par type
            issues = {
                "error": 0,
                "warning": 0,
                "refactor": 0,
                "convention": 0,
                "fatal": 0,
                "information": 0
            }

            for msg in messages:
                msg_type = msg.get("type", "unknown")
                if msg_type in issues:
                    issues[msg_type] += 1

            print(f"\n📊 Résultats pylint:")
            print(f"  Erreurs: {issues['error']}")
            print(f"  Avertissements: {issues['warning']}")
            print(f"  Refactoring: {issues['refactor']}")
            print(f"  Conventions: {issues['convention']}")
            print(f"  Fatales: {issues['fatal']}")

            # Afficher les 10 premiers problèmes
            if messages:
                print(f"\n⚠️ Top problèmes (premier 10):")
                for msg in messages[:10]:
                    print(f"  - [{msg.get('type')}] {msg.get('module')}: {msg.get('message')}")

            return {
                "status": "completed",
                "issues": issues,
                "messages": messages,
                "total": len(messages)
            }

        except FileNotFoundError:
            print("❌ pylint non installé. Exécutez: pip install pylint")
            return {"status": "not_installed"}
        except Exception as e:
            print(f"❌ Erreur pylint: {e}")
            return {"status": "error", "error": str(e)}

    def run_flake8(self) -> Dict:
        """Exécute flake8 sur le code source."""
        print("\n" + "=" * 60)
        print("🔍 FLAKE8 - Vérification de style PEP 8")
        print("=" * 60)

        try:
            cmd = [
                "flake8",
                "--config=.flake8",
                "--format=json",
                str(self.src_dir),
                str(self.tests_dir),
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.root_dir
            )

            try:
                messages = json.loads(result.stdout) if result.stdout else []
            except json.JSONDecodeError:
                messages = []

            # Compter les erreurs par code
            errors_by_code = {}
            for msg in messages:
                code = msg.get("code", "unknown")
                errors_by_code[code] = errors_by_code.get(code, 0) + 1

            print(f"\n📊 Résultats flake8:")
            print(f"  Total problèmes: {len(messages)}")
            if errors_by_code:
                print(f"  Erreurs par code:")
                for code, count in sorted(errors_by_code.items()):
                    print(f"    - {code}: {count}")

            # Afficher les 10 premiers
            if messages:
                print(f"\n⚠️ Top problèmes (premier 10):")
                for msg in messages[:10]:
                    print(f"  - {msg.get('filename')}:{msg.get('line_number')}: {msg.get('code')} {msg.get('text')}")

            return {
                "status": "completed",
                "messages": messages,
                "errors_by_code": errors_by_code,
                "total": len(messages)
            }

        except FileNotFoundError:
            print("❌ flake8 non installé. Exécutez: pip install flake8")
            return {"status": "not_installed"}
        except Exception as e:
            print(f"❌ Erreur flake8: {e}")
            return {"status": "error", "error": str(e)}

    def run_bandit(self) -> Dict:
        """Exécute bandit (analyse de sécurité)."""
        print("\n" + "=" * 60)
        print("🔒 BANDIT - Analyse de sécurité")
        print("=" * 60)

        try:
            cmd = [
                "bandit",
                "-r",
                str(self.src_dir),
                "-f", "json",
                "--exclude", str(self.tests_dir),
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.root_dir
            )

            try:
                data = json.loads(result.stdout) if result.stdout else {"results": [], "metrics": {}}
            except json.JSONDecodeError:
                data = {"results": [], "metrics": {}}

            results = data.get("results", [])

            # Compter par sévérité
            severities = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
            for issue in results:
                severity = issue.get("severity", "LOW")
                if severity in severities:
                    severities[severity] += 1

            print(f"\n📊 Résultats bandit:")
            print(f"  Critique (HIGH): {severities['HIGH']}")
            print(f"  Moyen (MEDIUM): {severities['MEDIUM']}")
            print(f"  Faible (LOW): {severities['LOW']}")

            # Afficher les problèmes critiques
            if results:
                print(f"\n⚠️ Problèmes de sécurité détectés:")
                for issue in results:
                    severity = issue.get("severity", "?")
                    test_id = issue.get("test_id", "?")
                    issue_text = issue.get("issue_text", "?")
                    print(f"  - [{severity}] {test_id}: {issue_text}")

            return {
                "status": "completed",
                "results": results,
                "severities": severities,
                "total": len(results)
            }

        except FileNotFoundError:
            print("❌ bandit non installé. Exécutez: pip install bandit")
            return {"status": "not_installed"}
        except Exception as e:
            print(f"❌ Erreur bandit: {e}")
            return {"status": "error", "error": str(e)}

    def run_coverage(self) -> Dict:
        """Exécute coverage sur les tests."""
        print("\n" + "=" * 60)
        print("🧪 COVERAGE - Couverture des tests")
        print("=" * 60)

        try:
            cmd = [
                "coverage",
                "run",
                "-m", "unittest",
                "discover", "tests/",
                "-v"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.root_dir,
                timeout=60
            )

            # Exécuter rapport
            cmd_report = ["coverage", "report"]
            result_report = subprocess.run(
                cmd_report,
                capture_output=True,
                text=True,
                cwd=self.root_dir
            )

            output = result_report.stdout
            print(f"\n{output}")

            # Parser le rapport
            match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', output)
            coverage_pct = int(match.group(1)) if match else 0

            print(f"\n📊 Couverture totale: {coverage_pct}%")

            return {
                "status": "completed",
                "coverage": coverage_pct,
                "output": output
            }

        except FileNotFoundError:
            print("❌ coverage non installé. Exécutez: pip install coverage")
            return {"status": "not_installed"}
        except Exception as e:
            print(f"❌ Erreur coverage: {e}")
            return {"status": "error", "error": str(e)}

    def generate_report(self):
        """Génère un rapport consolidé."""
        print("\n" + "=" * 60)
        print("📄 Génération du rapport")
        print("=" * 60)

        report_path = self.reports_dir / "ANALYSIS_REPORT.md"

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# RAPPORT D'ANALYSE DE SÉCURITÉ ET QUALITÉ\n\n")
            f.write("**Date** : 27 mai 2026\n")
            f.write("**Projet** : Librairie ABC\n")
            f.write("**Version** : 1.0.0\n\n")

            # Résumé
            f.write("## 📊 Résumé\n\n")

            pylint_total = self.results["pylint"].get("total", 0) if self.results["pylint"] else 0
            flake8_total = self.results["flake8"].get("total", 0) if self.results["flake8"] else 0
            bandit_total = self.results["bandit"].get("total", 0) if self.results["bandit"] else 0
            coverage = self.results["coverage"].get("coverage", 0) if self.results["coverage"] else 0

            f.write(f"| Métrique | Valeur |\n")
            f.write(f"|----------|--------|\n")
            f.write(f"| **Pylint - Problèmes** | {pylint_total} |\n")
            f.write(f"| **Flake8 - Erreurs de style** | {flake8_total} |\n")
            f.write(f"| **Bandit - Problèmes de sécurité** | {bandit_total} |\n")
            f.write(f"| **Coverage - Couverture tests** | {coverage}% |\n\n")

            # Détails Pylint
            f.write("## 🔍 PYLINT - Analyse de qualité\n\n")
            if self.results["pylint"] and self.results["pylint"].get("status") == "completed":
                issues = self.results["pylint"].get("issues", {})
                f.write(f"- Erreurs: {issues.get('error', 0)}\n")
                f.write(f"- Avertissements: {issues.get('warning', 0)}\n")
                f.write(f"- Refactoring: {issues.get('refactor', 0)}\n")
                f.write(f"- Conventions: {issues.get('convention', 0)}\n")
                f.write(f"- **Total**: {self.results['pylint'].get('total', 0)}\n\n")

            # Détails Flake8
            f.write("## 🔍 FLAKE8 - Vérification de style\n\n")
            if self.results["flake8"] and self.results["flake8"].get("status") == "completed":
                f.write(f"**Total**: {self.results['flake8'].get('total', 0)} problèmes\n\n")

            # Détails Bandit
            f.write("## 🔒 BANDIT - Analyse de sécurité\n\n")
            if self.results["bandit"] and self.results["bandit"].get("status") == "completed":
                severities = self.results["bandit"].get("severities", {})
                f.write(f"- Critique (HIGH): {severities.get('HIGH', 0)}\n")
                f.write(f"- Moyen (MEDIUM): {severities.get('MEDIUM', 0)}\n")
                f.write(f"- Faible (LOW): {severities.get('LOW', 0)}\n")
                f.write(f"- **Total**: {self.results['bandit'].get('total', 0)}\n\n")

            # Coverage
            f.write("## 🧪 COVERAGE - Couverture des tests\n\n")
            if self.results["coverage"] and self.results["coverage"].get("status") == "completed":
                f.write(f"**Couverture globale**: {self.results['coverage'].get('coverage', 0)}%\n\n")

            # Recommandations
            f.write("## 💡 Recommandations\n\n")
            f.write("1. **Réduire la complexité** des fonctions\n")
            f.write("2. **Ajouter des docstrings** aux fonctions publiques\n")
            f.write("3. **Améliorer la couverture** des tests\n")
            f.write("4. **Corriger les violations** de style\n")
            f.write("5. **Auditer** les problèmes de sécurité\n\n")

        print(f"\n✅ Rapport généré: {report_path}")

    def run_all(self):
        """Exécute tous les analyseurs."""
        print("\n" + "=" * 60)
        print("🚀 DÉMARRAGE DE L'ANALYSE DE SÉCURITÉ ET QUALITÉ")
        print("=" * 60)

        self.results["pylint"] = self.run_pylint()
        self.results["flake8"] = self.run_flake8()
        self.results["bandit"] = self.run_bandit()
        self.results["coverage"] = self.run_coverage()

        self.generate_report()

        print("\n" + "=" * 60)
        print("✅ ANALYSE COMPLÈTE")
        print("=" * 60)
        print(f"\nRapport sauvegardé: reports/ANALYSIS_REPORT.md")


if __name__ == "__main__":
    analyzer = CodeAnalyzer()
    analyzer.run_all()
