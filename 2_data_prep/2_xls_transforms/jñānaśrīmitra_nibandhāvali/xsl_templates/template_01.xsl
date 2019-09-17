<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="teiHeader" />

<xsl:template match="back" />

<xsl:template match="comment()" />

<xsl:template match="note[@n]|note[@type='public']" />

<xsl:template match="epigraph">
<p>
<xsl:value-of select="."/>
</p>
</xsl:template>

<xsl:template match="pb[@ed='jnams']" />


<!-- 
<xsl:value-of select="."/>
</xsl:template>
 -->

</xsl:stylesheet>