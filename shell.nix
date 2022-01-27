{
  pkgs ? import <nixpkgs> {},
  snapfaasSha256 ? "1rcqsid11ddlc4v33cw2fvxzywmm7s1rq36j3awi3qn1gwx2fvvp",
  snapfaasRev ? "4f37b2e6b90d7f2ce76d70d9b0790c7b3739eb8a",
  snapfaasSrc ? pkgs.fetchFromGitHub {
    owner = "princeton-sns";
    repo = "snapfaas";
    rev = snapfaasRev;
    sha256 = snapfaasSha256;
  },
  release ? false
}:

with pkgs;
let
  snapfaas = (import snapfaasSrc { inherit pkgs release; }).snapfaas;
in mkShell {
  buildInputs = [ lkl snapfaas lmdb ];
  shellHook = ''
    # Mark variables which are modified or created for export.
    set -a
    source ${toString ./.env}
    set +a
  '';
}
