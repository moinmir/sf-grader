{
  pkgs ? import <nixpkgs> {},
  snapfaasSha256 ? "0kr0j4zv9lmjfqbcm2py20ib6wjxj1s2s3983h24in98zhmpyja0",
  snapfaasRev ? "7396f0929ae2f00c9098d68f7da4d6abc6c053d9",
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
