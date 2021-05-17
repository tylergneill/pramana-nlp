<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="supplied">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="unclear">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="lb[not(@break)]">
<xsl:text> </xsl:text>
</xsl:template>

<xsl:template match="l">
<xsl:text> </xsl:text>
<xsl:value-of select="."/>
<xsl:text> </xsl:text>
</xsl:template>

<xsl:template match="quote[@type='base-text']">
<xsl:text>"</xsl:text>
<xsl:value-of select="."/>
<xsl:text>" (</xsl:text>
<xsl:value-of select="@xml:id"/>
<xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="q">
<xsl:text>"</xsl:text>
<xsl:value-of select="."/>
<xsl:text>"</xsl:text>
</xsl:template>

<xsl:template match="head|label[@type='head']|label[@type='trailer']">

〈<xsl:value-of select="."/>〉

</xsl:template>

</xsl:stylesheet>
